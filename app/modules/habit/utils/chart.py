from __future__ import annotations

import io
from typing import Sequence

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


def build_pie_chart(labels: Sequence[str], values: Sequence[int], title: str) -> bytes:
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.pie(values, labels=labels, autopct='%1.0f%%', startangle=90)
    ax.set_title(title)
    ax.axis('equal')
    buffer = io.BytesIO()
    plt.tight_layout()
    fig.savefig(buffer, format='png', dpi=160, bbox_inches='tight')
    plt.close(fig)
    buffer.seek(0)
    return buffer.getvalue()
