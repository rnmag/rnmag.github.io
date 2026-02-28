import glob
import re
import traceback
import os
from bs4 import BeautifulSoup, NavigableString, Tag

def convert_single_file(input_filename, output_filename):
    with open(input_filename, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')

    markdown_blocks = []
    notes = soup.find_all('div', class_='noteText')

    for note in notes:
        # CLEAN TEXT EXTRACTION ----
        # Stop reading the content of the div if we hit a header tag.
        # This prevents reading the *next* chapter title as part of *this* quote
        # due to malformed HTML in Kindle exports.
        quote_parts = []
        for child in note.contents:
            if isinstance(child, Tag) and child.name in ['h2', 'h3', 'h1', 'div']:
                break
            if isinstance(child, NavigableString):
                quote_parts.append(str(child))
            elif isinstance(child, Tag) and child.name == 'br':
                quote_parts.append('\n')
        
        quote_text = "".join(quote_parts).strip()
        if not quote_text: 
            continue

        # FIND METADATA (Backwards Search) ----
        # Use find_previous to look backwards in the DOM for the nearest headers
        chapter_tag = note.find_previous('h2', class_='sectionHeading')
        meta_tag = note.find_previous('h3', class_='noteHeading')

        chapter = chapter_tag.get_text().strip() if chapter_tag else "Unknown Chapter"

        location_str = ""
        if meta_tag:
            # Extract only digits from strings like "Posição 2054"
            match = re.search(r'(?:Posição|Position)\s+(\d+)', meta_tag.get_text())
            if match:
                location_str = f" (Location {match.group(1)})"

        # FORMATTING ----
        # Add markdown blockquote symbols
        fmt_quote = quote_text.replace('\n', '\n> ')
        block = f"> {fmt_quote}\n> \n> **{chapter}**{location_str}"
        markdown_blocks.append(block)

    # Write the output file
    if markdown_blocks:
        with open(output_filename, 'w', encoding='utf-8') as f:
            f.write("\n\n---\n\n".join(markdown_blocks))
    
    return len(markdown_blocks)

def main():
    # Define the pattern to look for
    suffix = "-Caderno de anotações.html"
    search_pattern = f"*{suffix}"
    
    # Find all matching files in the current directory
    files = glob.glob(search_pattern)

    if not files:
        print(f"No files found ending in '{suffix}'")
        return

    print(f"Found {len(files)} file(s). Starting batch conversion...\n")

    for input_file in files:
        try:
            # Generate output filename: "Infinite Jest - highlights.md"
            book_name = input_file.replace(suffix, "")
            output_file = f"{book_name} - highlights.md"
            
            count = convert_single_file(input_file, output_file)
            print(f"[OK] {book_name}: {count} highlights -> {output_file}")
            
        except Exception:
            print(f"[ERROR] Failed to convert: {input_file}")
            traceback.print_exc()

if __name__ == "__main__":
    main()

    input("\nPress Enter to exit...")