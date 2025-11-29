export interface ProjectManiaRequest {
  intent: string;
  variables: string[];
  template_type: 'general' | 'crewai' | 'autogen';
  prompt_length: 'low' | 'medium' | 'high';
  api_key?: string | null;
  password?: string | null;
  selected_model?: string;
  selected_groq_model?: string | null;
}

export interface ProjectManiaResponse {
  final_template: string;
  metadata: Record<string, unknown>;
}

export const generateProjectManiaTemplate = async (
  payload: ProjectManiaRequest
): Promise<ProjectManiaResponse> => {
  const response = await fetch('https://promptnova.onrender.com/project-mania/generate', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(payload),
  });

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({ detail: `HTTP error! status: ${response.status}` }));
    throw new Error(errorData.detail || 'Failed to generate template.');
  }


  return response.json();
};
