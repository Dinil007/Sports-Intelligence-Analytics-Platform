"""Centralized card styles for recommendation components.

Enterprise dark theme — badge styles kept for lightweight inline span rendering.
Card containers use native Streamlit container borders.
"""

SPORTA_CARD_CSS = """
<style>
.sporta-badge {
    display: inline-flex;
    align-items: center;
    padding: 4px 10px;
    border-radius: 9999px;
    font-size: 0.75rem;
    font-weight: 700;
    letter-spacing: 0.05em;
    text-transform: uppercase;
    margin-right: 6px;
}

.sporta-badge.elite {
    background: rgba(239, 68, 68, 0.2);
    color: #fca5a5;
    border: 1px solid rgba(239, 68, 68, 0.4);
}

.sporta-badge.high {
    background: rgba(249, 115, 22, 0.2);
    color: #fdba74;
    border: 1px solid rgba(249, 115, 22, 0.4);
}

.sporta-badge.medium {
    background: rgba(234, 179, 8, 0.2);
    color: #fde047;
    border: 1px solid rgba(234, 179, 8, 0.4);
}

.sporta-badge.low {
    background: rgba(34, 197, 94, 0.2);
    color: #86efac;
    border: 1px solid rgba(34, 197, 94, 0.4);
}
.badge-center {
    text-align: center;
    margin-top: 4px;
    margin-bottom: 4px;
}

</style>
"""


def get_card_css() -> str:
    """Return the centralized CSS for recommendation badges."""
    return SPORTA_CARD_CSS
