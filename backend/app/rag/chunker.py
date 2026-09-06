from typing import List


class RecursiveCharacterChunker:
    def __init__(self, chunk_size: int = 500, chunk_overlap: int = 100, separators: List[str] = None):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.separators = separators or ["\n\n", "\n", ". ", " ", ""]

    def split_text(self, text: str) -> List[str]:
        if not text:
            return []

        chunks = []
        current_text = text.strip()
        
        # Simple robust sliding window chunker
        start = 0
        text_len = len(current_text)
        
        while start < text_len:
            end = min(start + self.chunk_size, text_len)
            
            # If not at the end of text, find nearest separator to break naturally
            if end < text_len:
                best_break = end
                for sep in self.separators:
                    pos = current_text.rfind(sep, start, end)
                    if pos != -1 and pos > start + (self.chunk_size // 2):
                        best_break = pos + len(sep)
                        break
                end = best_break
                
            chunk = current_text[start:end].strip()
            if chunk:
                chunks.append(chunk)
                
            if end >= text_len:
                break
                
            start = max(start + 1, end - self.chunk_overlap)
            
        return chunks
