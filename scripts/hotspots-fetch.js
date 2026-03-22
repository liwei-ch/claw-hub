// 热点信息抓取脚本
const axios = require('axios');
const cheerio = require('cheerio');
const { execSync } = require('child_process');

// 配置
const CONFIG = {
  sources: [
    {
      name: '财联社',
      url: 'https://www.cls.cn/',
      selector: '.js-article-list .article-item'
    },
    {
      name: '问财网',
      url: 'https://www.iwencai.com/',
      selector: '.hot-concept .item'
    },
    {
      name: '韭菜公社',
      url: 'https://www.jiucaigongshe.com/',
      selector: '.hot-topic-list .topic-item'
    }
  ],
  pushGroup: 'oc_9aa475cf3c0aeeb88c3e33e0b7a8b3b8'
};

// 抓取单个来源
async function fetchSource(source) {
  try {
    const response = await axios.get(source.url, {
      headers: {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
      },
      timeout: 10000
    });
    
    const $ = cheerio.load(response.data);
    const items = [];
    
    $(source.selector).each((i, el) => {
      if (i < 5) { // 每个来源最多取5条
        const title = $(el).text().trim();
        if (title && title.length > 10) {
          items.push(title);
        }
      }
    });
    
    return { name: source.name, items };
  } catch (error) {
    console.error(`抓取${source.name}失败:`, error.message);
    return { name: source.name, items: [] };
  }
}

// 推送消息到飞书
function pushToFeishu(content) {
  try {
    execSync(`openclaw message send --to chat:${CONFIG.pushGroup} --message "${content.replace(/"/g, '\\"')}"`);
  } catch (error) {
    console.error('推送失败:', error.message);
  }
}

// 主函数
async function main(type = 'morning') {
  console.log(`开始执行${type === 'morning' ? '早间' : '午间'}热点抓取任务`);
  
  // 抓取所有来源
  const results = await Promise.all(CONFIG.sources.map(fetchSource));
  
  // 整理内容
  let content = type === 'morning' ? '🌅 【早间投资热点汇总】\n\n' : '☀️ 【午间投资热点汇总】\n\n';
  
  let totalItems = 0;
  for (const result of results) {
    if (result.items.length > 0) {
      content += `### 📌 ${result.name}\n`;
      result.items.forEach((item, i) => {
        content += `${i + 1}. ${item}\n`;
        totalItems++;
      });
      content += '\n';
    }
  }
  
  // 风险提示
  content += '⚠️ 风险提示：以上信息来源于公开网络，仅供参考，不构成投资建议。\n';
  content += '股市有风险，投资需谨慎。';
  
  // 推送
  if (totalItems >= 3) {
    pushToFeishu(content);
    console.log('推送完成');
  } else {
    console.log('信息不足，取消推送');
    pushToFeishu('今日热点信息不足，暂不推送。');
  }
}

// 执行
const type = process.argv[2] || 'morning';
main(type).catch(console.error);
