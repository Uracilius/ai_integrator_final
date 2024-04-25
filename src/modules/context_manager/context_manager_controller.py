from .src.db.mongo import initialize_mongo_db, add_mongo_data, get_mongo_data, rollback_mongo_data
from .src.db.postgres import initialize_postgres_db, add_postgres_data, get_postgres_data, rollback_postgres_data
from .src.db.chroma import add_chroma_data, get_chroma_closest_data, rollback_chroma_data
from ..shared.DTO.context_data import ContextDTO
from ..shared.DTO.chroma_response import ChromaResponse

def add_chat_to_context(conversation_log: str, context_data: ContextDTO) -> ContextDTO:
    initialize_mongo_db()  
    initialize_postgres_db()

    mongo_id = None
    postgres_id = None
    try:
        # MongoDB Add
        mongo_id = add_mongo_data(conversation_log)
        context_data.convo_id = mongo_id

        # PostgreSQL Add"
        postgres_id = add_postgres_data(context_data)
        context_data.id = postgres_id

        # ChromaDB Add
        add_chroma_data(context_data.id, context_data.tags, context_data.user_id)

    except Exception as e:
        # Rollback in reverse order of commits
        if postgres_id:
            rollback_postgres_data(postgres_id)
        if mongo_id:
            rollback_mongo_data(mongo_id)
            
        # Reraise the exception to inform the caller of the failure
        raise Exception(f"Failed to complete the transaction of adding a conversation: {str(e)}")

    return context_data

def get_convo_context(tags, user_id):
    initialize_mongo_db()  
    initialize_postgres_db()
    print(user_id)
    chroma_response = ChromaResponse(get_chroma_closest_data(tags, user_id))
    closest_item = chroma_response.get_first_item()

    context = get_postgres_data(closest_item['id'])
    chat_log = get_mongo_data(context.convo_id)

    return context, chat_log['text']

if __name__ == "__main__":
    
    #print(add_chat_to_context("Testing quadruple threat", ContextDTO()))
    #rollback_chroma_data('8')
    print(get_convo_context('conversation', '12345'))
    #print(get_context(1))
