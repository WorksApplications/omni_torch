import torch
import torch.nn as nn
    
class MSE_Loss(nn.Module):
    def __init__(self, sum_dim=None, sqrt=False, dimension_warn=0):
        super().__init__()
        self.sum_dim = sum_dim
        self.sqrt = sqrt
        self.dimension_warn = dimension_warn
    
    def forward(self, x, y):
        assert x.shape == y.shape
        if self.sum_dim:
            mse_loss = torch.sum((x - y) ** 2, dim=self.sum_dim)
        else:
            mse_loss = torch.sum((x - y) ** 2)
        if self.sqrt:
            mse_loss = torch.sqrt(mse_loss)
        mse_loss = torch.sum(mse_loss) / mse_loss.nelement()
        if len(mse_loss.shape) > self.dimension_warn:
            raise ValueError("The shape of mse loss should be a scalar, but you can skip this"
                             "error by change the dimension_warn explicitly.")
        return mse_loss
    
class KL_Divergence(nn.Module):
    def __init__(self, sum_dim=None, sqrt=False, dimension_warn=0):
        super().__init__()
        self.sum_dim = sum_dim
        self.sqrt = sqrt
        self.dimension_warn = dimension_warn
        
    def forward(self, x, y):
        
        # Normalize
        x = x.view(x.size(0), x.size(1), -1)
        x = x / x.norm(1, dim=-1).unsqueeze(-1)
        y = y.view(y.size(0), y.size(1), -1)
        y = y / y.norm(1, dim=-1).unsqueeze(-1)
        loss = torch.sum((y * (y.log() - x.log())), dim=self.sum_dim)
        return loss.squeeze()

class Triplet_Loss(nn.Module):
    def __init__(self, mode, margin=0.2, engine=MSE_Loss, weighted=False,
                 sum_dim=None, sqrt=False):
        """
        :param mode: minus and divide mode
        :param margin: a mininum distance to keep the triplet distance discriminative
        :param weighted: amplify the wrong case more
        """
        super().__init__()
        self.mode = mode
        self.margin = margin
        self.weighted = weighted
        self.mse = engine(sum_dim, sqrt, dimension_warn=1)
    
    def forward(self, positive, anchor, negative):
        if self.mode == "minus":
            dist = self.mse(anchor, positive) - self.mse(anchor, negative) + self.margin
        elif self.mode == "divide":
            dist = self.mse(anchor, positive) + 1 / (self.mse(anchor, negative) + self.margin)
        else:
            raise NotImplementedError
        if self.weighted:
            weight = dist / dist.norm(1)
            dist = torch.sum(dist * weight) / dist.nelement()
        else:
            dist = torch.sum(dist) / dist.nelement()
        while len(dist.shape) > 0:
            print("actual loss shape is larger than zero, sum is somewhat wrong. fixing it...")
            dist = torch.sum(dist)
        return dist