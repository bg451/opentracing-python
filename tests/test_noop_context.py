# Copyright (c) 2015 Uber Technologies, Inc.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

from __future__ import absolute_import
from opentracing import TraceContext, TraceContextSource
from opentracing import TraceContextMarshaler, TraceContextUnmarshaler


def test_context():
    ctx = TraceContext()
    assert ctx.get_metadata('x') is None
    ctx.set_metadata('X_y', 'value').\
        set_metadata('ZZ', 'value2')
    assert ctx.get_metadata('X_y') is None


def test_context_source():
    singleton = TraceContextSource.singleton_noop_trace_context
    source = TraceContextSource()
    assert source.new_root_trace_context() == singleton
    child, meta = source.new_child_trace_context(
        parent_trace_context=singleton)
    assert child == singleton
    assert meta is None


def test_marshaller():
    singleton = TraceContextSource.singleton_noop_trace_context
    m = TraceContextMarshaler()
    x, y = m.marshal_trace_context_binary(trace_context=singleton)
    assert x == bytearray()
    assert y == bytearray()
    x, y = m.marshal_trace_context_str_dict(trace_context=singleton)
    assert x == {}
    assert y == {}


def test_unmarshaller():
    singleton = TraceContextSource.singleton_noop_trace_context
    m = TraceContextUnmarshaler()
    ctx = m.unmarshal_trace_context_binary(trace_context_id=None,
                                           metadata=None)
    assert singleton == ctx
    ctx = m.unmarshal_trace_context_str_dict(trace_context_id=None,
                                             metadata=None)
    assert singleton == ctx