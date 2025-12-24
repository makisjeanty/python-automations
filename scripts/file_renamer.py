#!/usr/bin/env python3
"""
File Renamer - Batch rename files with various patterns
Supports: adding prefixes/suffixes, replacing text, sequential numbering, date stamps
"""

import os
import sys
from pathlib import Path
from datetime import datetime
import argparse
import re


def add_prefix(filename, prefix):
    """Add prefix to filename"""
    return f"{prefix}{filename}"


def add_suffix(filename, suffix):
    """Add suffix before file extension"""
    name, ext = os.path.splitext(filename)
    return f"{name}{suffix}{ext}"


def replace_text(filename, old_text, new_text):
    """Replace text in filename"""
    return filename.replace(old_text, new_text)


def add_sequential_number(filename, number, digits=3):
    """Add sequential number to filename"""
    name, ext = os.path.splitext(filename)
    return f"{name}_{str(number).zfill(digits)}{ext}"


def add_date_stamp(filename, date_format="%Y%m%d"):
    """Add current date to filename"""
    name, ext = os.path.splitext(filename)
    date_str = datetime.now().strftime(date_format)
    return f"{name}_{date_str}{ext}"


def sanitize_filename(filename):
    """Remove special characters and replace spaces with underscores"""
    name, ext = os.path.splitext(filename)
    # Remove special characters, keep only alphanumeric, dots, hyphens, underscores
    name = re.sub(r'[^\w\s-]', '', name)
    # Replace spaces with underscores
    name = re.sub(r'\s+', '_', name)
    # Remove multiple underscores
    name = re.sub(r'_+', '_', name)
    return f"{name}{ext}"


def rename_files(directory, pattern, dry_run=True, recursive=False):
    """
    Rename files in directory based on pattern
    
    Args:
        directory: Target directory
        pattern: Dictionary with rename pattern options
        dry_run: If True, only show what would be renamed
        recursive: If True, process subdirectories
    """
    path = Path(directory)
    
    if not path.exists():
        print(f"❌ Error: Directory '{directory}' does not exist")
        return
    
    # Get files
    if recursive:
        files = [f for f in path.rglob('*') if f.is_file()]
    else:
        files = [f for f in path.iterdir() if f.is_file()]
    
    if not files:
        print(f"⚠️  No files found in '{directory}'")
        return
    
    print(f"\n{'🔍 DRY RUN MODE - No files will be renamed' if dry_run else '✅ RENAMING FILES'}")
    print(f"📁 Directory: {directory}")
    print(f"📊 Files found: {len(files)}\n")
    
    renamed_count = 0
    
    for idx, file_path in enumerate(sorted(files), start=1):
        old_name = file_path.name
        new_name = old_name
        
        # Apply transformations in order
        if pattern.get('sanitize'):
            new_name = sanitize_filename(new_name)
        
        if pattern.get('replace'):
            old_text, new_text = pattern['replace']
            new_name = replace_text(new_name, old_text, new_text)
        
        if pattern.get('prefix'):
            new_name = add_prefix(new_name, pattern['prefix'])
        
        if pattern.get('suffix'):
            new_name = add_suffix(new_name, pattern['suffix'])
        
        if pattern.get('sequential'):
            new_name = add_sequential_number(new_name, idx, pattern.get('digits', 3))
        
        if pattern.get('date'):
            new_name = add_date_stamp(new_name, pattern.get('date_format', '%Y%m%d'))
        
        # Only rename if name changed
        if new_name != old_name:
            new_path = file_path.parent / new_name
            
            # Check if target file already exists
            if new_path.exists():
                print(f"⚠️  Skipping '{old_name}' - target '{new_name}' already exists")
                continue
            
            print(f"  {old_name}")
            print(f"  → {new_name}\n")
            
            if not dry_run:
                try:
                    file_path.rename(new_path)
                    renamed_count += 1
                except Exception as e:
                    print(f"❌ Error renaming '{old_name}': {e}\n")
    
    print(f"\n{'Would rename' if dry_run else 'Renamed'} {renamed_count} file(s)")
    
    if dry_run:
        print("\n💡 Run with --execute flag to actually rename files")


def main():
    parser = argparse.ArgumentParser(
        description='Batch rename files with various patterns',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Add prefix (dry run)
  python file_renamer.py /path/to/files --prefix "IMG_"
  
  # Add sequential numbers and execute
  python file_renamer.py /path/to/files --sequential --execute
  
  # Replace text in filenames
  python file_renamer.py /path/to/files --replace "old" "new" --execute
  
  # Sanitize filenames (remove special chars, replace spaces)
  python file_renamer.py /path/to/files --sanitize --execute
  
  # Add date stamp
  python file_renamer.py /path/to/files --date --execute
  
  # Combine multiple operations
  python file_renamer.py /path/to/files --sanitize --prefix "photo_" --sequential --execute
        """
    )
    
    parser.add_argument('directory', help='Directory containing files to rename')
    parser.add_argument('--prefix', help='Add prefix to filenames')
    parser.add_argument('--suffix', help='Add suffix to filenames (before extension)')
    parser.add_argument('--replace', nargs=2, metavar=('OLD', 'NEW'), 
                       help='Replace text in filenames')
    parser.add_argument('--sequential', action='store_true', 
                       help='Add sequential numbers')
    parser.add_argument('--digits', type=int, default=3, 
                       help='Number of digits for sequential numbering (default: 3)')
    parser.add_argument('--date', action='store_true', 
                       help='Add date stamp (YYYYMMDD)')
    parser.add_argument('--date-format', default='%Y%m%d', 
                       help='Date format (default: %%Y%%m%%d)')
    parser.add_argument('--sanitize', action='store_true', 
                       help='Remove special characters and replace spaces with underscores')
    parser.add_argument('--recursive', '-r', action='store_true', 
                       help='Process subdirectories recursively')
    parser.add_argument('--execute', action='store_true', 
                       help='Actually rename files (default is dry run)')
    
    args = parser.parse_args()
    
    # Build pattern dictionary
    pattern = {}
    
    if args.sanitize:
        pattern['sanitize'] = True
    if args.prefix:
        pattern['prefix'] = args.prefix
    if args.suffix:
        pattern['suffix'] = args.suffix
    if args.replace:
        pattern['replace'] = args.replace
    if args.sequential:
        pattern['sequential'] = True
        pattern['digits'] = args.digits
    if args.date:
        pattern['date'] = True
        pattern['date_format'] = args.date_format
    
    if not pattern:
        print("❌ Error: No rename pattern specified")
        parser.print_help()
        sys.exit(1)
    
    rename_files(
        args.directory,
        pattern,
        dry_run=not args.execute,
        recursive=args.recursive
    )


if __name__ == '__main__':
    main()
