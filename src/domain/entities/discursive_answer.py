from src.domain.value_objects.uuid_identifier import UuidIdentifier

class DiscursiveAnswer:
  def __init__(
    self,
    id: UuidIdentifier,
    id_question: UuidIdentifier,
    id_student: UuidIdentifier,
    answer: str,
    grade: int | None,
    feedback: str | None,
    created_at: int,
    corrected_at: int | None
  ):
    if not id or not isinstance(id, UuidIdentifier):
      raise ValueError("id must be an UuidIdentifier")
    if not id_question or not isinstance(id_question, UuidIdentifier):
      raise ValueError("id_question must be an UuidIdentifier")
    if not id_student or not isinstance(id_student, UuidIdentifier):
      raise ValueError("id_student must be an UuidIdentifier")
    if not answer:
        raise ValueError("answer is required")
    if created_at is None:
        raise ValueError("created_at is required")

    self.id = id
    self.id_question = id_question
    self.id_student = id_student
    self.answer = answer
    self.grade = grade
    self.feedback = feedback
    self.created_at = created_at
    self.corrected_at = corrected_at

  def __str__(self):
    return f"<DiscursiveAnswer {self.id} - student: {self.id_student}, grade: {self.grade}>"
