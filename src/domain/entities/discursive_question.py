from src.domain.value_objects.uuid_identifier import UuidIdentifier

class DiscursiveQuestion:
  def __init__(
    self,
    id: UuidIdentifier,
    authorId: UuidIdentifier,
    title: str,
    prompt: str,
    expected_answer: str,
    criteria: str,
    tags: list[str],
    topic: str,
    difficulty: str,
    grade_level: int,
    created_at: float,
  ):
    if not id or not isinstance(id, UuidIdentifier):
      raise ValueError("id must be an UuidIdentifier")
    if not authorId or not isinstance(authorId, UuidIdentifier):
      raise ValueError("authorId must be an UuidIdentifier")
    if not title:
      raise ValueError("title is required")
    if not prompt:
      raise ValueError("prompt is required")
    if not expected_answer:
      raise ValueError("expected_answer is required")
    if not criteria:
      raise ValueError("criteria is required")
    if not tags or not isinstance(tags, list):
      raise ValueError("tags must be a non-empty list")
    if not topic:
      raise ValueError("topic is required")
    if not difficulty:
      raise ValueError("difficulty is required")
    if grade_level is None:
      raise ValueError("grade_level is required")
    if created_at is None:
      raise ValueError("created_at is required")
    self.id = id
    self.authorId = authorId
    self.title = title
    self.prompt = prompt
    self.expected_answer = expected_answer
    self.criteria = criteria
    self.tags = tags
    self.topic = topic
    self.difficulty = difficulty
    self.grade_level = grade_level
    self.created_at = created_at