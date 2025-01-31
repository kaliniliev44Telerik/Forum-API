from fastapi import  APIRouter, Response, Header
from data.models import  Conversation
from services import conversation_service
from common.auth import verify_authenticated_user
from services.topic_service import exists

conversation_router = APIRouter(prefix='/api/conversations')

@conversation_router.get('')
def get_conversations(token: str = Header()):
    verify_authenticated_user(token)
    user_id = token.split(";")[0]
    result = conversation_service.get_all(user_id)
    if result is None:
        return Response(status_code=404, content="No conversations found.")
    else:
        return result
    
@conversation_router.get('/{id}')
def get_conversation_by_id(id: int, token: str = Header()):
    if not conversation_service.exists(id):
        return Response(status_code=404, content="Conversation not found.")

    verify_authenticated_user(token)
    user_id = int(token.split(";")[0])
    result = conversation_service.get_by_id(id,user_id)
    if result is None:
        return Response(status_code=401, content="no no no")
    else:
        return result



