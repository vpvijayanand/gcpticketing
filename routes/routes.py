from flask import Blueprint, request, jsonify
from models.ticket_model import TicketCreation
from utils.translate import detect_and_translate_text

ticket_route = Blueprint('ticket_route', __name__)

# Route for creating a new ticket
@ticket_route.route('/create_ticket', methods=['POST'])
def create_ticket():
    try:
        # Extract data from the request body
        data = request.json
        original_text = data.get('problem_description')
        language = data.get('language', 'en')  # Default to English if not provided
        category = data.get('category')
        severity = data.get('severity')

        # Step 1: Detect and translate the text if needed
        translated_text, detected_language = detect_and_translate_text(original_text)

        # Step 2: Create a ticket and assign it to an agent
        ticket_db = TicketCreation()
        ticket_db.create_ticket(original_text, detected_language, category, severity)
        ticket_db.close_connection()

        return jsonify({
            'message': 'Ticket created successfully',
            'translated_text': translated_text,
            'original_language': detected_language
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 400
