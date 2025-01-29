// Code generated by wit-bindgen-go. DO NOT EDIT.

// Package consumer represents the imported interface "wasmcloud:messaging/consumer@0.2.0".
package consumer

import (
	"gitea.rebus.ninja/lore/wasm-nats-producer-client/gen/wasmcloud/messaging/types"
	"github.com/bytecodealliance/wasm-tools-go/cm"
)

// BrokerMessage represents the type alias "wasmcloud:messaging/consumer@0.2.0#broker-message".
//
// See [types.BrokerMessage] for more information.
type BrokerMessage = types.BrokerMessage

// Request represents the imported function "request".
//
// Perform a request operation on a subject
//
//	request: func(subject: string, body: list<u8>, timeout-ms: u32) -> result<broker-message,
//	string>
//
//go:nosplit
func Request(subject string, body cm.List[uint8], timeoutMs uint32) (result cm.Result[BrokerMessageShape, BrokerMessage, string]) {
	subject0, subject1 := cm.LowerString(subject)
	body0, body1 := cm.LowerList(body)
	timeoutMs0 := (uint32)(timeoutMs)
	wasmimport_Request((*uint8)(subject0), (uint32)(subject1), (*uint8)(body0), (uint32)(body1), (uint32)(timeoutMs0), &result)
	return
}

// Publish represents the imported function "publish".
//
// Publish a message to a subject without awaiting a response
//
//	publish: func(msg: broker-message) -> result<_, string>
//
//go:nosplit
func Publish(msg BrokerMessage) (result cm.Result[string, struct{}, string]) {
	msg0, msg1, msg2, msg3, msg4, msg5, msg6 := lower_BrokerMessage(msg)
	wasmimport_Publish((*uint8)(msg0), (uint32)(msg1), (*uint8)(msg2), (uint32)(msg3), (uint32)(msg4), (*uint8)(msg5), (uint32)(msg6), &result)
	return
}
