import torch
import numpy as np


def cos_similarity(a, b):
    """
    Computes the cosine similarity.
    """
    if not isinstance(a, torch.Tensor):
        a = torch.tensor(np.array(a)).float()

    if not isinstance(b, torch.Tensor):
        b = torch.tensor(np.array(b)).float()

    if len(a.shape) == 1:
        a = a.unsqueeze(0)

    if len(b.shape) == 1:
        b = b.unsqueeze(0)
    a_norm = torch.nn.functional.normalize(a, p=2, dim=1)
    b_norm = torch.nn.functional.normalize(b, p=2, dim=1)
    
    return torch.mm(a_norm, b_norm.transpose(0, 1))