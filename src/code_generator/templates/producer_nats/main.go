//go:generate go run github.com/bytecodealliance/wasm-tools-go/cmd/wit-bindgen-go generate --world hello --out gen ./wit
package main

import (
	"fmt"
	"net/http"
	"io"

	logger "gitea.rebus.ninja/lore/wasm-nats-producer-client/gen/wasi/logging/logging"
	"gitea.rebus.ninja/lore/wasm-nats-producer-client/gen/wasmcloud/messaging/consumer"
	"gitea.rebus.ninja/lore/wasm-nats-producer-client/gen/wasmcloud/messaging/handler"
	"gitea.rebus.ninja/lore/wasm-nats-producer-client/gen/wasmcloud/messaging/types"
	"github.com/bytecodealliance/wasm-tools-go/cm"
	"go.wasmcloud.dev/component/net/wasihttp"
)

type messagingConsumerAdapter struct {
	Publish func(msg types.BrokerMessage) (result cm.Result[string, struct{}, string])
}

// NOTE(lxf): this is overridden in tests
var messagingConsumer = &messagingConsumerAdapter{
	Publish: consumer.Publish,
} 


func init() {
	wasihttp.HandleFunc(handleHttp)
	handler.Exports.HandleMessage = handleMessage
}

func handleHttp(w http.ResponseWriter, r *http.Request) {

	value, err := io.ReadAll(r.Body)

	if err != nil {
		fmt.Fprintf(w, "Error, invalid request body\n") 
		return
	}

	if handleRequest(string(value)) {
		fmt.Fprintf(w, "Message sent!\n")
	} else {
		fmt.Fprintf(w, "Error, coudln't send message\n")
	}
}

func handleMessage(msg types.BrokerMessage) cm.Result[string, struct{}, string]{

	logger.Log(logger.LevelInfo,"MessageHandler", "Received message on subject" + msg.Subject)

	arg := cm.LiftString[string, *uint8, uint8](msg.Body.Data(), uint8(msg.Body.Len()))

	if handleRequest(arg) {
		cm.OK[cm.Result[string, struct{}, string]](struct{}{})
	}

	return cm.Err[cm.Result[string, struct{}, string]]("Couldn't send message to topic")
}

func handleRequest(arg string) bool {
	
	// TODO implement the logic to get the destination topic from the config
	// dest_topic := config.GetAll()
	dest_topic := "{{ dest_topic }}"

	result := exec_task(arg)

	// Send reply
	reply := types.BrokerMessage{
		Subject: dest_topic,
		Body:    cm.ToList([]byte(result)),
		ReplyTo: cm.None[string](),
	}
	res := messagingConsumer.Publish(reply)
	if res.IsErr() {
		logger.Log(logger.LevelError, "MessageHandler", "Failed to send reply, error: " + *res.Err())
		return false
	}

	return true
}

// Since we don't run this program like a CLI, the `main` function is empty. Instead,
// we call the `handleRequest` function when an HTTP request is received.
func main() {}
