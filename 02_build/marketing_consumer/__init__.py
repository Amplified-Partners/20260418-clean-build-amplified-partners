"""marketing_consumer — governed downstream consumer of shared substrate.

Marketing is the first downstream consumer. It reads from Brain packets
via context_packet_id / brain_packet_id. It does NOT fork the schema.

Marketing-Kaizen emits candidates, never canonical truth.

Signed-by: Devon-d493 | 2026-05-19 | devin-d49302e4179d43d0892997a7f3a9f57f
"""
