package com.uber.tchannel.messages;

public class CallRequestContinue extends Message {
    public CallRequestContinue(long id) {
        super(id, MessageType.CallRequestContinue);
    }
}
