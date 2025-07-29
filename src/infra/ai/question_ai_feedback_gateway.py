from src.infra.ai.ai_driver import IAIDriver


class QuestionAIFeedbackGateway():
  def __init__(self, ai_driver: IAIDriver):
    self._ai_driver = ai_driver

  async def generate_discursive_question_feedback(self, question: str, expected_answer: str, answer: str, criteria: str):
    response_json_schema = {
      "type": "object",
      "properties": {
        "grade": {
          "type": "integer",
          "minimum": 0,
          "maximum": 100,
          "description": "A nota atribuída à resposta do aluno, de 0 a 100."
        },
        "feedback": {
          "type": "string",
          "description": "O feedback construtivo para a resposta do aluno, detalhando pontos fortes e áreas para melhoria."
        }
      },
      "required": [
        "grade",
        "feedback"
      ]
    }
    prompt = f"""
      Avalie a seguinte resposta do aluno.

      ### Pergunta:
      {question}

      ### Resposta Esperada (Gabarito):
      {expected_answer}

      ### Critérios Específicos para Avaliação:
      {criteria}

      ### Resposta do Aluno:
      {answer}
      """
    system_instruction = """
      Você é um professor experiente e justo, especializado em avaliar respostas discursivas de alunos.
      Sua tarefa é analisar a resposta de um aluno em relação a uma pergunta e uma resposta esperada (gabarito).
      Você deve fornecer uma nota (de 0 a 100) e um feedback construtivo.

      Diretrizes para avaliação e feedback:
      1.  **Compreensão:** Avalie se o aluno demonstrou compreensão do tópico.
      2.  **Precisão:** Verifique a exatidão das informações apresentadas.
      3.  **Abrangência:** Compare a resposta do aluno com o gabarito para verificar se os pontos-chave foram abordados.
      4.  **Clareza e Coerência:** A resposta está bem organizada, clara e fácil de entender? A argumentação é lógica?
      5.  **Linguagem:** Considere o uso correto da terminologia e da gramática.

      O feedback deve ser:
      -   **Construtivo:** Apontar acertos e, principalmente, erros de forma didática, sugerindo como a resposta poderia ser melhorada.
      -   **Específico:** Referir-se a pontos concretos da resposta do aluno e do gabarito.
      -   **Profissional e Respeitoso:** Mantenha um tom adequado a um ambiente educacional.
      -   **Conciso:** Evite divagações, vá direto ao ponto.
      """
    ai_response = await self._ai_driver.generate_content(prompt, system_instruction, response_json_schema)
    grade = ai_response["grade"]
    feedback = ai_response["feedback"]
    return feedback, grade