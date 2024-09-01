#%%
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from nlp.llm_interface import call_llm

def test_call_llm():
    assert type(call_llm("What is 3 * 12? then subtract 22 from the result")) == str


# %%
