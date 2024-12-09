from typing import Dict
import PyPDF2
import docx
import io

class DocumentProcessor:
    async def process_document(self, file_content: bytes, file_type: str) -> str:
        try:
            if file_type == 'application/pdf':
                return self._process_pdf(file_content)
            elif file_type == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
                return self._process_docx(file_content)
            elif file_type == 'text/plain':
                return file_content.decode('utf-8')
            else:
                raise ValueError("Unsupported file type")
        except Exception as e:
            raise Exception(f"Error processing document: {str(e)}")
    
    
    def _process_pdf(self, content: bytes) -> str:
        try:
            pdf_reader = PyPDF2.PdfReader(io.BytesIO(content))
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()
            return text
        except Exception as e:
            raise Exception(f"Error processing PDF: {str(e)}")
        
    def _process_docx(self, content: bytes) -> str:
        try:
            doc = docx.Document(io.BytesIO(content))
            return " ".join([paragraph.text for paragraph in doc.paragraphs])
        except Exception as e:
            raise Exception(f"Error processing DOCX: {str(e)}")