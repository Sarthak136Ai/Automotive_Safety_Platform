import logging

# Configure logger
logger = logging.getLogger(__name__)

# Lazy-loaded pipeline variable
_summarizer = None

def get_summarizer():
    global _summarizer
    if _summarizer is None:
        try:
            from transformers import pipeline
            logger.info("Loading HuggingFace BART-Large-CNN summarizer...")
            _summarizer = pipeline(
                "summarization",
                model="facebook/bart-large-cnn",
                device=-1  # Force CPU to avoid CUDA conflicts in standard setups
            )
            logger.info("BART model loaded successfully.")
        except Exception as e:
            logger.error(f"Failed to load BART summarizer: {e}")
            _summarizer = None
    return _summarizer

def generate_summary_headline(text, fast=True):
    text = str(text).strip()

    if not text:
        return "General vehicle safety recall"

    # Truncate very long text
    text = text[:1024]

    # Fast extractive summarization (ideal for bulk pipeline processing)
    if fast:
        # Extract first sentence or segment
        sentences = [s.strip() for s in text.split('.') if s.strip()]
        if not sentences:
            return "General vehicle safety recall"
        
        headline = sentences[0]
        # Clean up double spaces or special chars
        import re
        headline = re.sub(r'\s+', ' ', headline)
        
        # Limit length to a reasonable headline size (e.g. 100 chars)
        if len(headline) > 100:
            headline = headline[:97].strip() + "..."
            
        # Capitalize first letter
        if headline:
            headline = headline[0].upper() + headline[1:]
            
        return headline

    # Full BART Summarization for live interactive requests
    summarizer_pipeline = get_summarizer()
    if summarizer_pipeline is None:
        return generate_summary_headline(text, fast=True)

    try:
        summary = summarizer_pipeline(
            text,
            max_length=25,
            min_length=8,
            do_sample=False
        )
        generated_summary = summary[0]["summary_text"]
        
        # Clean and format
        generated_summary = generated_summary.replace(" .", ".").strip()
        if generated_summary:
            generated_summary = generated_summary[0].upper() + generated_summary[1:]
            
        return generated_summary
    except Exception as e:
        logger.error(f"Summarization Error: {e}")
        # Fallback to fast extractive
        return generate_summary_headline(text, fast=True)