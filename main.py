"""
Main entry point - redirects to app.py for Railway compatibility
"""
import os
from app import create_interface


def main():
    """Launch the Gradio app"""
    app = create_interface()
    # Use Railway's PORT environment variable if available, otherwise default to 7860
    port = int(os.environ.get("PORT", 7860))
    app.launch(server_name="0.0.0.0", server_port=port)


if __name__ == "__main__":
    main()
