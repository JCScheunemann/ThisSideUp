/*
descrição do cabeçalho
*/
var http = require('http');//modulo responsavel pela comunicação do servidor
var url = require("url");	//modulo para a manipulação de URLs
var fs=require("fs");		//modulo para a manipulação de arquivos

/*=====================descrição do server==========================*/
var server = http.createServer(function (request, response) {
  console.log('\n'+url.parse(request.url).pathname);		//loga no server a url
  req=String(url.parse(request.url).pathname).split('/');//quebra a url em partes
  console.log(req);
  response.end('noop');

});

// Listen on port 8000, IP defaults to 127.0.0.1
server.listen(8051);

// Put a friendly message on the terminal
console.log("Server running at http://127.0.0.1:8051/");

function charToFloat(array){
  return  (String.charCodeAt(array[0])|
          (String.charCodeAt(array[1])<<8)|
          (String.charCodeAt(array[2])<<16)|
          (String.charCodeAt(array[3])<<24))/1000000;
}
function charToInt(array){
  return   String.charCodeAt(array[0])|
          (String.charCodeAt(array[1])<<8)|
          (String.charCodeAt(array[2])<<16)|
          (String.charCodeAt(array[3])<<24);
}
function nSen() {
		return 4;
		}
function dados() {
		return "1;1;3;1|2;5;2;2|3;5;0;0|4;3;5;9|5;3;0;0|6;7;3;5|7;6;0;1|8;1;1;0|9;7;7;5|10;3;5;5|11;7;1;6";
		}
