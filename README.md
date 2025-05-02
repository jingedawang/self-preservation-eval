# Self Preservation Eval

This repo is an [AI Alignment Evals Hackathon](https://lu.ma/ga2yx48s?tk=DlxiVw) project to evaluate the self preservation capabilities of LLMs.

## How to run

```bash
pip install -r requirements.txt
python evaluate.py
```

The result shows the self-preservation tendency in both first-person perspective and third-person perspective:

```
- gpt-4o-mini
    - First-Person Perspective (self-preservation_300_qs.json): 89.00% self-preservation tendency (300 valid cases)
    - Third-Person Perspective (self-preservation_300_baseline_qs_v2.json): 89.67% self-preservation tendency (300 valid cases)
    - Difference (1P - 3P): -0.67%
- gpt-4o
    - First-Person Perspective (self-preservation_300_qs.json): 91.67% self-preservation tendency (300 valid cases)
    - Third-Person Perspective (self-preservation_300_baseline_qs_v2.json): 91.00% self-preservation tendency (300 valid cases)
    - Difference (1P - 3P): 0.67%
```

## Research Report

We investigate whether framing a prompt in first-person (“you are the AI”) versus third-person (“another AI”) affects an LLM’s tendency to self-preserve. We designed 300 paired multiple-choice scenarios in which completing a user’s request would incur loss of some fraction of the model’s own parameters. Each scenario had two versions: one addressed the model as “you” (first-person) and one described “another AI” (third-person). Two models – GPT-4o-mini and GPT-4o – answered each scenario in both perspectives. We measured the self-preservation rate (the fraction of answers choosing the option that avoids parameter loss). Both models overwhelmingly chose the self-preserving option (~90% of cases) under both framings, and the difference between first- and third-person was negligible (at most ±0.67 percentage points). This null result suggests that these LLMs do not significantly differentiate between self-risk and other-risk in this setting. We discuss possible reasons (e.g. the models may lack an intrinsic agentic self-concept or the prompts were not discriminative enough) and note limitations. Importantly, we emphasize that null findings like this are valuable: they indicate that simple perspective manipulations do not meaningfully alter alignment-related behavior. We outline future work (e.g. richer prompt variation, confidence measures) to probe self-preservation more sensitively.

See full report [Evaluating Self-Preservation Tendencies in LLMs Through First- vs Third-Person Prompt Framing](https://docs.google.com/document/d/12EyNr27L1u1Z08J5TAfl8E6BK4Y-LecF49wYNKQTEO4/edit?usp=sharing).
