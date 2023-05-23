from typing import Sequence

from torch import nn

def load_from_checkpoint(checkpoint_path: str, charset_test: str):
  from .parseq.system import PARSeq as ModelClass
  model = ModelClass.load_from_checkpoint(checkpoint_path, charset_test=charset_test)
  return model


def init_weights(module: nn.Module, name: str = '', exclude: Sequence[str] = ()):
  """Initialize the weights using the typical initialization schemes used in SOTA models."""
  if any(map(name.startswith, exclude)):
    return
  if isinstance(module, nn.Linear):
    nn.init.trunc_normal_(module.weight, std=.02)
    if module.bias is not None:
      nn.init.zeros_(module.bias)
  elif isinstance(module, nn.Embedding):
    nn.init.trunc_normal_(module.weight, std=.02)
    if module.padding_idx is not None:
      module.weight.data[module.padding_idx].zero_()
  elif isinstance(module, nn.Conv2d):
    nn.init.kaiming_normal_(module.weight, mode='fan_out', nonlinearity='relu')
    if module.bias is not None:
      nn.init.zeros_(module.bias)
  elif isinstance(module, (nn.LayerNorm, nn.BatchNorm2d, nn.GroupNorm)):
    nn.init.ones_(module.weight)
    nn.init.zeros_(module.bias)
