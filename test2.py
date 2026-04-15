
def test():
    resume_text = 'hello'
    prompt = f'''{{
      "summary": {{
        "background": "full",
        "bullets": ["ex1"]
      }}
    }}
    Resume: {resume_text}'''
    print('SUCCESS')
test()
