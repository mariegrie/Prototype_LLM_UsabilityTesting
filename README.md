# Prototype_LLM_UsabilityTesting
Repository for HICSS 2026 Paper: Towards Simulating User Behavior for Automating Usability Tests by Employing Large Language Models

## Components of the Prototype
### GPTInteraction
* LLM call for interaction choice
* Prompt includes screenshot of the current page, static prompt providing context, task (provided with initial user input) and history (extended with every iteration)

### GPTFindElement
* LLM call for element locator
* Prompt includes HTML code fetched with every iteration, static prompt detailing required output structure and interaction choice from the first LLM call

### TestRunner
* Bringing it all together - enabling the iterative testing process
* Automated Web Interaction
* Capturing Screenshot of every iteration
* Writing results to files


### GPT Requirements
```python
pip install openai
```

```python
pip install python-dotenv
```

```python
pip install tenacity
```

```python
pip install tiktoken
```

```python
pip install Image
```

### Web Interaction Requirements

```python
pip install selenium 
```

```python
pip install bs4
```
