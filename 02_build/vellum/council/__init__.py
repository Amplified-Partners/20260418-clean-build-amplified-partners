"""Council of Three — heterogeneous frontier-model logic-checking panel.

Architecture from peer-reviewed evidence (476-line literature review, May 2026):
- Three genuinely heterogeneous frontier models (GPT-5.5 + Claude Opus 4.7 + Gemini 3.1 Pro)
- Round 1 independent (blind), Round 2 only if disagreement
- Inter-model disagreement is the primary uncertainty signal
- Selective routing (council only on uncertain/high-stakes queries)
- Majority vote with minority report (upgrade to Optimal Weight after 50+ labelled outcomes)

Devon-b5dc | 2026-05-14
"""
