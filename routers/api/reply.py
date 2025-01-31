from fastapi import APIRouter, Response, Header,Form
from fastapi.responses import RedirectResponse
from common.auth import get_user_or_raise_401, verify_authenticated_user
from data.models import Reply
from services import reply_service, vote_service

reply_router = APIRouter(prefix='/api/replies')

@reply_router.get('')
def get_replies(sort: str | None = None, sort_by: str | None = None, search: str | None = None):
    result = reply_service.get_all(search)
    if result is None:
        return Response(status_code=404, content="No replies found.")
    else:
        if sort and (sort == 'asc' or sort == 'desc'):
            return reply_service.sort_replies(result, reverse=sort == 'desc', attribute=sort_by)
        else:
            return result

@reply_router.post('')
def create_reply(content: str = Form(...), topics_id: int = Form(...),token: str = Form(...)):

    user_id = int(token.split(";")[0])
    verify_authenticated_user(token)
    reply_id,create_datetime = reply_service.create(content, topics_id, user_id)
    if reply_id:
        formatted_created_at = create_datetime.strftime('%Y-%m-%d %H:%M:%S')
        return Response(status_code=200,content=f"reply with id: {reply_id} and content:' {content}' was created at {formatted_created_at}.")
    else:
        return Response(status_code=404, content="Access is restricted.")


@reply_router.get('/all_votes')
def get_votes(token: str = Header()):
    verify_authenticated_user(token)
    return vote_service.get_all()


@reply_router.put('/{id}/upvote')
def vote(id:int, token: str = Header()):
    verify_authenticated_user(token)
    user_id = int(token.split(";")[0])
    return vote_service.upvote(id,user_id)
    
@reply_router.put('/{id}/downvote')
def vote(id:int, token: str = Header()):
    verify_authenticated_user(token)
    user_id = int(token.split(";")[0])
    return vote_service.upvote(id,user_id)
    