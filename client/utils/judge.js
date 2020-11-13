const judgeurl = value => {
  return  value=="found"?0
          :value=='study'?1
          :value=='play_'?2
          :value=='secon'?3
          :value=='postg'?4
          :value=='paper'?5
          :value=='code_'?6
          :7;
}

const judgestatus = status => {
  return  status=="没找到"?'已找到'
          :status=='已找到'?'没找到'
          :status=='没卖'?'已售'
          :'没卖';
}

module.exports = {
  judgeurl: judgeurl,
  judgestatus: judgestatus,
}