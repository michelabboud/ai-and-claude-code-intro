"""
Document Loader - Load documents from various formats for RAG systems.

Supports:
- Markdown (.md)
- Text files (.txt)
- JSON (.json)
- PDF (.pdf)
- Word documents (.docx)
- HTML (.html)
"""

import os
import json
from pathlib import Path
from typing import List, Dict, Optional
import pypdf
import docx
from bs4 import BeautifulSoup
from datetime import datetime


class DocumentLoader:
    """
    Universal document loader for RAG systems.

    Loads documents from various formats and returns standardized format:
    {
        'content': str,
        'metadata': {
            'source': str,
            'filename': str,
            'type': str,
            'loaded_at': str
        }
    }
    """

    def __init__(self):
        self.supported_extensions = ['.md', '.txt', '.json', '.pdf', '.docx', '.html']

    def load_file(self, filepath: str) -> Optional[Dict]:
        """
        Load a single file.

        Args:
            filepath: Path to file

        Returns:
            Document dict or None if unsupported format
        """
        path = Path(filepath)

        if not path.exists():
            raise FileNotFoundError(f"File not found: {filepath}")

        extension = path.suffix.lower()

        if extension not in self.supported_extensions:
            print(f"⚠️  Unsupported file type: {extension}")
            return None

        # Load based on file type
        if extension == '.md' or extension == '.txt':
            content = self._load_text(path)
        elif extension == '.json':
            content = self._load_json(path)
        elif extension == '.pdf':
            content = self._load_pdf(path)
        elif extension == '.docx':
            content = self._load_docx(path)
        elif extension == '.html':
            content = self._load_html(path)
        else:
            return None

        return {
            'content': content,
            'metadata': {
                'source': str(path.absolute()),
                'filename': path.name,
                'type': extension[1:],  # Remove leading dot
                'loaded_at': datetime.now().isoformat()
            }
        }

    def load_directory(
        self,
        directory: str,
        recursive: bool = True,
        extensions: Optional[List[str]] = None
    ) -> List[Dict]:
        """
        Load all documents from a directory.

        Args:
            directory: Path to directory
            recursive: Whether to search subdirectories
            extensions: List of extensions to load (e.g., ['.md', '.txt'])
                       If None, loads all supported types

        Returns:
            List of document dicts
        """
        dir_path = Path(directory)

        if not dir_path.exists():
            raise FileNotFoundError(f"Directory not found: {directory}")

        if not dir_path.is_dir():
            raise ValueError(f"Not a directory: {directory}")

        # Determine which extensions to load
        extensions_to_load = extensions if extensions else self.supported_extensions

        # Find all matching files
        documents = []
        pattern = "**/*" if recursive else "*"

        for ext in extensions_to_load:
            for filepath in dir_path.glob(f"{pattern}{ext}"):
                if filepath.is_file():
                    try:
                        doc = self.load_file(str(filepath))
                        if doc:
                            documents.append(doc)
                            print(f"✅ Loaded: {filepath.name}")
                    except Exception as e:
                        print(f"❌ Error loading {filepath.name}: {e}")

        print(f"\n📚 Loaded {len(documents)} documents from {directory}")
        return documents

    def _load_text(self, path: Path) -> str:
        """Load plain text or markdown file."""
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()

    def _load_json(self, path: Path) -> str:
        """Load JSON file and convert to text."""
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Convert JSON to readable text
        if isinstance(data, dict):
            # If it's a structured document with 'content' field, use that
            if 'content' in data:
                return data['content']
            # Otherwise, pretty-print the JSON
            return json.dumps(data, indent=2)
        elif isinstance(data, list):
            # Join list items with newlines
            return '\n\n'.join(str(item) for item in data)
        else:
            return str(data)

    def _load_pdf(self, path: Path) -> str:
        """Load PDF file and extract text."""
        text_parts = []

        with open(path, 'rb') as f:
            pdf_reader = pypdf.PdfReader(f)

            for page_num, page in enumerate(pdf_reader.pages, 1):
                text = page.extract_text()
                if text.strip():
                    text_parts.append(f"--- Page {page_num} ---\n{text}")

        return '\n\n'.join(text_parts)

    def _load_docx(self, path: Path) -> str:
        """Load Word document and extract text."""
        doc = docx.Document(path)

        text_parts = []
        for paragraph in doc.paragraphs:
            if paragraph.text.strip():
                text_parts.append(paragraph.text)

        return '\n\n'.join(text_parts)

    def _load_html(self, path: Path) -> str:
        """Load HTML file and extract text."""
        with open(path, 'r', encoding='utf-8') as f:
            html_content = f.read()

        soup = BeautifulSoup(html_content, 'html.parser')

        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()

        # Get text
        text = soup.get_text()

        # Clean up whitespace
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = '\n'.join(chunk for chunk in chunks if chunk)

        return text


def load_markdown_files(directory: str) -> List[Dict]:
    """
    Convenience function to load only Markdown files.

    Args:
        directory: Path to directory

    Returns:
        List of document dicts
    """
    loader = DocumentLoader()
    return loader.load_directory(directory, extensions=['.md'])


def load_text_files(directory: str) -> List[Dict]:
    """
    Convenience function to load only text files.

    Args:
        directory: Path to directory

    Returns:
        List of document dicts
    """
    loader = DocumentLoader()
    return loader.load_directory(directory, extensions=['.txt'])


# Example usage
if __name__ == "__main__":
    # Create sample data directory for testing
    sample_dir = Path("./data/sample_docs")
    sample_dir.mkdir(parents=True, exist_ok=True)

    # Create sample markdown file
    sample_md = sample_dir / "kubernetes-intro.md"
    with open(sample_md, 'w') as f:
        f.write("""# Kubernetes Introduction

Kubernetes (K8s) is an open-source container orchestration platform that automates deployment, scaling, and management of containerized applications.

## Key Concepts

- **Pod**: Smallest deployable unit
- **Service**: Network abstraction for pods
- **Deployment**: Manages pod replicas
- **ConfigMap**: Configuration data
- **Secret**: Sensitive data

## Common Commands

```bash
kubectl get pods
kubectl get services
kubectl logs <pod-name>
kubectl describe pod <pod-name>
```
""")

    # Create sample text file
    sample_txt = sample_dir / "runbook-high-cpu.txt"
    with open(sample_txt, 'w') as f:
        f.write("""High CPU Alert Runbook

Symptom: CPU usage above 80% for more than 5 minutes

Immediate Actions:
1. Check which process is consuming CPU
   kubectl top pods -n <namespace>

2. Review recent deployments
   kubectl rollout history deployment/<name>

3. Scale up if needed
   kubectl scale deployment <name> --replicas=5

Investigation:
- Check application logs for errors
- Review recent code changes
- Analyze traffic patterns

Resolution:
- Optimize code if application issue
- Increase resource limits if infrastructure issue
- Consider horizontal pod autoscaling
""")

    print("="*80)
    print("Document Loader Demo")
    print("="*80)

    # Initialize loader
    loader = DocumentLoader()

    # Load all documents from directory
    documents = loader.load_directory("./data/sample_docs", recursive=True)

    # Display loaded documents
    print(f"\n{'='*80}")
    print("Loaded Documents:")
    print('='*80)

    for i, doc in enumerate(documents, 1):
        print(f"\nDocument {i}:")
        print(f"  Filename: {doc['metadata']['filename']}")
        print(f"  Type: {doc['metadata']['type']}")
        print(f"  Size: {len(doc['content'])} characters")
        print(f"  Preview: {doc['content'][:150]}...")

    # Load only markdown files
    print(f"\n{'='*80}")
    print("Loading Only Markdown Files:")
    print('='*80)

    md_documents = load_markdown_files("./data/sample_docs")
    print(f"Loaded {len(md_documents)} Markdown documents")
