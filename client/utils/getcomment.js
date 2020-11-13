const comment = value => {
  var comment = [];
  for(var i=0;i< value.length;i++)
  {
  comment = comment.concat(value[i][0]);
  }
  return comment;
}

const reply = value_reply => {
  var reply = [];
  for(var i=0;i< value_reply.length;i++)
  {
  //comment = comment.concat(value_reply[i][0]);
  for(var j=1;j<value_reply[i].length;j++)
    {
    reply = reply.concat(value_reply[i][j]);
    }
  }
  return reply;
}

module.exports = {
  comment: comment,
  reply: reply,
}