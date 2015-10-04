var TelegramBot = require('node-telegram-bot-api');

var token = '125345847:AAFKJFwaETnTK_pEQXQ2Hqwx8bnLFV5oo2E';
// Setup polling way
var bot = new TelegramBot(token, {polling: true});

// Setup webhooks way
var options = {
  webHook: {
    port: 443,
    key: __dirname+'/key.pem',
    cert: __dirname+'/crt.pem'
  }
};

//var bot = new TelegramBot(token, options);
//bot.setWebHook('IP:PORT/botBOT_TOKEN', __dirname+'/crt.pem');
// --> End Setup webhooks way

bot.on('text', function (msg) {
  var chatId = msg.chat.id;
  bot.sendMessage(chatId, "Bonjour! Je ne comprends pas encore toutes les subtilités de votre langues ;)");
  // bot.sendPhoto(chatId, photo, {caption: 'Lovely kittens'});
});


