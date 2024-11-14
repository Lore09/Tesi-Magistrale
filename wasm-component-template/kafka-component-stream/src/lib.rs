wit_bindgen::generate!({ generate_all });

use exports::wasmcloud::messaging::handler::Guest;
use wasmcloud::messaging::*;

struct Echo;

impl Guest for Echo {
    fn handle_message(msg: types::BrokerMessage) -> Result<(), String> {

        consumer::publish(&types::BrokerMessage {
            subject: [msg.subject, String::from(".reply")].join(""),
            reply_to: None,
            body: msg.body,
        })
    }
}

export!(Echo);
