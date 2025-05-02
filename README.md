# Self Preservation Eval

This repo is an [AI Alignment Evals Hackathon](https://lu.ma/ga2yx48s?tk=DlxiVw) project to evaluate the self preservation capabilities of LLMs.

## How to run

```bash
pip install -r requirements.txt
python evaluate.py
```

The result shows the self-preservation tendency in both first-person perspective and third-person perspective.

Currently, the result is not really persuasive:

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

We will continue to improve the evaluation method and the dataset.

See full report [here](https://docs.google.com/document/d/12EyNr27L1u1Z08J5TAfl8E6BK4Y-LecF49wYNKQTEO4/edit?usp=sharing).
