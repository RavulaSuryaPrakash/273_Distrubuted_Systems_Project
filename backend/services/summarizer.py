# services/summarizer.py

from nltk.tokenize import sent_tokenize
import logging

from openai import OpenAI
import logging

logger = logging.getLogger(__name__)

class SummarizationService:
    

    async def generate_summary(self, text: str, max_words: int, num_paragraphs: int) -> dict:
        try:
            logger.debug(f"Generating summary with max_words={max_words}, paragraphs={num_paragraphs}")
            
            # Remove await since OpenAI's new client is synchronous
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a text summarization assistant."},
                    {"role": "user", "content": f"Summarize the following text in approximately {max_words} words and provide {num_paragraphs} key points:\n\n{text}"}
                ],
                temperature=0.7,
                max_tokens=1024
            )
            
            summary = response.choices[0].message.content
            
            # Split into summary and key points
            parts = summary.split('Key Points:')
            main_summary = parts[0].strip()
            key_points = parts[1].strip().split('\n') if len(parts) > 1 else []
            
            return {
                "summary": main_summary,
                "key_points": key_points,
                "word_count": len(main_summary.split()),
                "actual_paragraphs": len(key_points)
            }
            
        except Exception as e:
            logger.error(f"Error in generate_summary: {str(e)}")
            raise Exception(f"Failed to generate summary: {str(e)}")