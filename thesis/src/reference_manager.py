import json
import os
import hashlib
from datetime import datetime

class ReferenceManager:
    def __init__(self, topic=""):
        # Create unique reference file per topic
        if topic:
            topic_hash = hashlib.md5(topic.encode()).hexdigest()[:8]
            self.ref_file = f"thesis/references_{topic_hash}.json"
        else:
            self.ref_file = "thesis/references.json"
        
        self.references = self._load_references()

    def _load_references(self):
        """Load references from JSON file."""
        if os.path.exists(self.ref_file):
            try:
                with open(self.ref_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading references: {e}")
                return {"references": []}
        return {"references": []}

    def _save_references(self):
        """Save references to JSON file."""
        try:
            os.makedirs(os.path.dirname(self.ref_file), exist_ok=True)
            with open(self.ref_file, 'w', encoding='utf-8') as f:
                json.dump(self.references, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving references: {e}")

    def add_reference(self, ref_data, chapter, ref_type="academic"):
        """
        Add a reference and track where it's used.
        ref_data: dict with title, authors, year, etc.
        """
        # Generate unique ID based on title
        ref_id = hashlib.md5(ref_data.get('title', 'untitled').encode()).hexdigest()[:8]
        
        # Check if reference already exists
        existing_ref = None
        for ref in self.references['references']:
            if ref['id'] == ref_id:
                existing_ref = ref
                break
        
        if existing_ref:
            # Update usage tracking
            if chapter not in existing_ref.get('used_in', []):
                existing_ref['used_in'].append(chapter)
        else:
            # Process authors to capture full details
            authors_list = ref_data.get('authors', [])
            if isinstance(authors_list, list):
                # Ensure we have author names (handle both dict and string formats)
                processed_authors = []
                for author in authors_list:
                    if isinstance(author, dict):
                        processed_authors.append(author.get('name', 'Unknown'))
                    else:
                        processed_authors.append(str(author))
            else:
                processed_authors = ['Unknown']
            
            # Add new reference
            new_ref = {
                "id": ref_id,
                "type": ref_type,
                "title": ref_data.get('title', 'Untitled'),
                "authors": processed_authors,  # Full author names
                "year": ref_data.get('year', 'n.d.'),
                "venue": ref_data.get('venue', ''),
                "abstract": ref_data.get('abstract', '')[:500] if ref_data.get('abstract') else '',  # Truncate abstract
                "url": ref_data.get('url', ''),
                "doi": ref_data.get('doi', ''),  # Capture DOI if available
                "used_in": [chapter],
                "added_date": datetime.now().isoformat()
            }
            self.references['references'].append(new_ref)
        
        self._save_references()

    def get_all_references(self):
        """Return all references."""
        return self.references['references']

    def format_reference(self, ref):
        """
        Format a single reference in Harvard style.
        Called by thesis_main.py when generating bibliography.
        """
        # Format authors
        if isinstance(ref.get('authors'), list) and ref['authors']:
            if ref['type'] == 'academic':
                authors = ", ".join([a.get('name', a) if isinstance(a, dict) else a for a in ref['authors']])
            else:
                authors = ref['authors'][0] if ref['authors'] else 'Unknown'
        else:
            authors = 'Unknown'
        
        # Format reference based on type
        if ref['type'] == 'academic':
            venue = ref.get('venue', 'Unknown Venue')
            doi = ref.get('doi', '')
            citation = f"{authors} ({ref['year']}) '{ref['title']}', {venue}."
            if doi:
                citation += f" DOI: {doi}"
        else:  # web
            url = ref.get('url', '')
            citation = f"'{ref['title']}' (n.d.) [Online]. Available at: {url}."
        
        return citation

    def generate_bibliography(self, output_file=None):
        """Generate a Harvard-style bibliography file."""
        if output_file is None:
            output_file = self.ref_file.replace('references_', 'Bibliography_').replace('.json', '.md')
        
        # Sort references by author last name
        sorted_refs = sorted(
            self.references['references'],
            key=lambda x: x.get('authors', ['Unknown'])[0] if isinstance(x.get('authors'), list) else 'Unknown'
        )
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("# Bibliography\n\n")
            f.write("## References Used in This Thesis\n\n")
            
            for ref in sorted_refs:
                citation = self.format_reference(ref)
                
                # Add usage info
                used_in = ", ".join(ref.get('used_in', []))
                
                f.write(f"- {citation}\n")
                f.write(f"  - *Used in: {used_in}*\n\n")
        
        print(f"📚 Bibliography generated: {output_file}")
        return output_file
