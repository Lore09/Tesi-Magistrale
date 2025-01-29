// Code generated by wit-bindgen-go. DO NOT EDIT.

// Package terminalstdout represents the imported interface "wasi:cli/terminal-stdout@0.2.0".
package terminalstdout

import (
	terminaloutput "gitea.rebus.ninja/lore/wasm-nats-stream-client/gen/wasi/cli/terminal-output"
	"github.com/bytecodealliance/wasm-tools-go/cm"
)

// TerminalOutput represents the imported type alias "wasi:cli/terminal-stdout@0.2.0#terminal-output".
//
// See [terminaloutput.TerminalOutput] for more information.
type TerminalOutput = terminaloutput.TerminalOutput

// GetTerminalStdout represents the imported function "get-terminal-stdout".
//
//	get-terminal-stdout: func() -> option<terminal-output>
//
//go:nosplit
func GetTerminalStdout() (result cm.Option[TerminalOutput]) {
	wasmimport_GetTerminalStdout(&result)
	return
}
