import json
import argparse
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
import sys

@dataclass
class FileStats:
    path: Path
    size_kb: float
    total_lines: int
    code_lines: int

@dataclass
class ExtensionStats:
    extension: str
    file_count: int
    total_lines: int
    code_lines: int
    total_size_kb: float
    max_lines_file: Optional[Path]
    max_lines_count: int

class CodeAnalyzer:
    def __init__(self):
        self.default_extensions = [
            '.py', '.js', '.java', '.cpp', '.c', '.html', '.css', '.md'
        ]
        self.language_names = {
            '.py': 'Python',
            '.js': 'JavaScript',
            '.java': 'Java',
            '.cpp': 'C++',
            '.c': 'C',
            '.html': 'HTML',
            '.css': 'CSS',
            '.md': 'Markdown',
            '.ts': 'TypeScript',
            '.rb': 'Ruby',
            '.php': 'PHP',
            '.go': 'Go',
            '.rs': 'Rust'
        }
    
    def get_language_name(self, extension: str) -> str:
        return self.language_names.get(extension, extension.upper())
    
    def is_code_file(self, file_path: Path, extensions: List[str]) -> bool:
        return file_path.suffix.lower() in extensions
    
    def count_lines(self, file_path: Path) -> Tuple[int, int]:
        """Возвращает (общее количество строк, количество строк кода)"""
        total_lines = 0
        code_lines = 0
        in_multiline_comment = False
        
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
                for line in file:
                    total_lines += 1
                    stripped_line = line.strip()
                    
                    if not stripped_line:
                        continue
                    
                    if in_multiline_comment:
                        if '*/' in stripped_line:
                            in_multiline_comment = False
                            after_comment = stripped_line.split('*/')[-1].strip()
                            if after_comment and not after_comment.startswith('//'):
                                code_lines += 1
                        continue
                    
                    if '/*' in stripped_line:
                        in_multiline_comment = True
                        before_comment = stripped_line.split('/*')[0].strip()
                        if before_comment:
                            code_lines += 1
                        continue
                    

                    if (stripped_line.startswith(('//', '#', '--')) or 
                        stripped_line.startswith('/*') or 
                        stripped_line.startswith('*') or
                        stripped_line.startswith('<!--')):
                        continue

                    code_lines += 1
        
        except (IOError, UnicodeDecodeError) as e:
            print(f"Предупреждение: не удалось прочитать файл {file_path}: {e}")
            return 0, 0
        
        return total_lines, code_lines
    
    def analyze_file(self, file_path: Path) -> Optional[FileStats]:
        try:
            size_kb = file_path.stat().st_size / 1024
            total_lines, code_lines = self.count_lines(file_path)
            
            return FileStats(
                path=file_path,
                size_kb=size_kb,
                total_lines=total_lines,
                code_lines=code_lines
            )
        except Exception as e:
            print(f"Ошибка при анализе файла {file_path}: {e}")
            return None
    
    def analyze_directory(self, project_path: str, extensions: Optional[List[str]] = None) -> Dict:
        if extensions is None:
            extensions = self.default_extensions

        normalized_extensions = []
        for ext in extensions:
            if not ext.startswith('.'):
                ext = '.' + ext
            normalized_extensions.append(ext.lower())
        
        project_path = Path(project_path)
        if not project_path.exists():
            raise ValueError(f"Путь {project_path} не существует")
        if not project_path.is_dir():
            raise ValueError(f"Путь {project_path} не является директорией")
        
        extension_stats = {ext: ExtensionStats(
            extension=ext,
            file_count=0,
            total_lines=0,
            code_lines=0,
            total_size_kb=0,
            max_lines_file=None,
            max_lines_count=0
        ) for ext in normalized_extensions}
        
        all_files_stats = []
        total_files = 0
        total_size_mb = 0
        total_lines = 0
        total_code_lines = 0
        
        print("Сканирование файлов...")
        
        for file_path in project_path.rglob('*'):
            if file_path.is_file() and self.is_code_file(file_path, normalized_extensions):
                file_stats = self.analyze_file(file_path)
                if file_stats is None:
                    continue
                
                all_files_stats.append({
                    'path': str(file_path),
                    'size_kb': round(file_stats.size_kb, 2),
                    'total_lines': file_stats.total_lines,
                    'code_lines': file_stats.code_lines,
                    'extension': file_path.suffix.lower()
                })
                
                ext = file_path.suffix.lower()
                if ext in extension_stats:
                    stats = extension_stats[ext]
                    stats.file_count += 1
                    stats.total_lines += file_stats.total_lines
                    stats.code_lines += file_stats.code_lines
                    stats.total_size_kb += file_stats.size_kb

                    if file_stats.total_lines > stats.max_lines_count:
                        stats.max_lines_count = file_stats.total_lines
                        stats.max_lines_file = file_path
                
                total_files += 1
                total_size_mb += file_stats.size_kb / 1024
                total_lines += file_stats.total_lines
                total_code_lines += file_stats.code_lines

        result = {
            'project_path': str(project_path.absolute()),
            'total_files': total_files,
            'total_size_mb': round(total_size_mb, 2),
            'total_lines': total_lines,
            'total_code_lines': total_code_lines,
            'analyzed_extensions': normalized_extensions,
            'by_extension': {},
            'files': all_files_stats
        }
        
        for ext, stats in extension_stats.items():
            if stats.file_count > 0:
                avg_lines = stats.total_lines / stats.file_count
                result['by_extension'][ext] = {
                    'file_count': stats.file_count,
                    'total_lines': stats.total_lines,
                    'code_lines': stats.code_lines,
                    'total_size_kb': round(stats.total_size_kb, 2),
                    'avg_lines_per_file': round(avg_lines, 1),
                    'max_lines_file': str(stats.max_lines_file.relative_to(project_path)) if stats.max_lines_file else None,
                    'max_lines_count': stats.max_lines_count,
                    'language_name': self.get_language_name(ext)
                }
        
        return result
    
    def print_report(self, analysis_result: Dict):
        print(f"\n[Анализ кодовой базы проекта: {analysis_result['project_path']}]")
        print("=" * 70)
        print()
        
        print("Общая статистика:")
        print(f"• Всего файлов с кодом: {analysis_result['total_files']:,}".replace(',', ' '))
        print(f"• Общий объем кода: {analysis_result['total_size_mb']} MB")
        print(f"• Общее количество строк: {analysis_result['total_lines']:,}".replace(',', ' '))
        print(f"• Логических строк кода: {analysis_result['total_code_lines']:,}".replace(',', ' '))
        print(f"• Анализируемые расширения: {', '.join(analysis_result['analyzed_extensions'])}")
        print()
        
        print("Детали по типам файлов:")
        for ext, stats in analysis_result['by_extension'].items():
            lang_name = stats.get('language_name', self.get_language_name(ext))
            print(f"[{lang_name}] ({ext})")
            print(f"  Файлов: {stats['file_count']}, "
                  f"Строк: {stats['total_lines']:,}, "
                  f"Средний размер: {stats['avg_lines_per_file']} строк/файл".replace(',', ' '))
            
            if stats['max_lines_file']:
                print(f"  Самый большой файл: {stats['max_lines_file']} "
                      f"({stats['max_lines_count']:,} строк)".replace(',', ' '))
            print()
    
    def save_to_json(self, analysis_result: Dict, output_file: str = "code_analysis_report.json"):
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(analysis_result, f, indent=2, ensure_ascii=False)
            print(f"✓ Отчет сохранен в файл: {output_file}")
        except Exception as e:
            print(f"✗ Ошибка при сохранении отчета: {e}")

def main():
    parser = argparse.ArgumentParser(description='Анализатор кодовой базы')
    parser.add_argument('project_path', help='Путь к корневой директории проекта')
    parser.add_argument('-e', '--extensions', nargs='+', 
                       help='Список расширений для анализа (например: .py .js .java)')
    parser.add_argument('-o', '--output', default='code_analysis_report.json',
                       help='Имя выходного JSON файла')
    
    args = parser.parse_args()
    
    analyzer = CodeAnalyzer()
    
    try:
        print("Запуск анализа кодовой базы...")
        result = analyzer.analyze_directory(args.project_path, args.extensions)
        
        analyzer.print_report(result)
        analyzer.save_to_json(result, args.output)
        
        print("\n Анализ завершен успешно!")
        
    except ValueError as e:
        print(f" Ошибка: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n Анализ прерван пользователем")
        sys.exit(1)
    except Exception as e:
        print(f" Неожиданная ошибка: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()