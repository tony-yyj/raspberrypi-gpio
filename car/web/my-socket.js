class MySocket {
    static _instance;
    static getInstance() {
        if (MySocket._instance) {
            return MySocket._instance;
        }
        MySocket._instance = new MySocket();
    }
    _ws;
    constructor() {
        this._ws = new WebSocket('ws://192.168.0.111:8765');
        this._ws.onopen = function(event) {
            console.log('connected to websocket server')
        }

    

    }
    

}

var mySocket = MySocket.getInstance();