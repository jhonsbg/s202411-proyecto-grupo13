import uuid
from .base_command import BaseCommannd
from ..models.post import Post, PostSchema
from ..session import Session
from ..errors.errors import InvalidParams, PostNotFoundError

class DeletePost(BaseCommannd):
  def __init__(self, post_id):
    if self.is_uuid(post_id):
      self.post_id = post_id
    else:
      raise InvalidParams()

  def execute(self):
    session = Session()
    post = session.query(Post).filter_by(id=self.post_id).first()
    if post is None:
      session.close()
      raise PostNotFoundError()

    session.delete(post)
    session.commit()

    session.close()

  def is_uuid(self, val):
      try:
        uuid.UUID(str(val))
        return True
      except ValueError:
        return False