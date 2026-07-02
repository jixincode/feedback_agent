import logging
import os
from datetime import datetime
from openai import OpenAI
from config import config
from prompt_templates import SYSTEM_PROMPT, USER_PROMPT_TEMPLATE

# 创建日志目录
log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logs')
os.makedirs(log_dir, exist_ok=True)

# 配置日志 - 同时输出到控制台和文件
log_filename = os.path.join(log_dir, f'feedback_{datetime.now().strftime("%Y%m%d")}.log')

# 创建 logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# 避免重复添加 handler
if not logger.handlers:
    # 文件处理器
    file_handler = logging.FileHandler(log_filename, encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    file_formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)

    # 控制台处理器
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)

class FeedbackAgent:
    def __init__(self):
        logger.info("=" * 60)
        logger.info("初始化 FeedbackAgent")
        logger.debug(f"API Base URL: {config.OPENAI_API_BASE}")
        logger.debug(f"API Key: {config.OPENAI_API_KEY[:10]}..." if config.OPENAI_API_KEY else "API Key 未配置")
        logger.debug(f"Model: {config.MODEL_NAME}")
        logger.debug(f"Max Tokens: {config.MAX_TOKENS}")
        logger.debug(f"Temperature: {config.TEMPERATURE}")

        try:
            self.client = OpenAI(
                api_key=config.OPENAI_API_KEY,
                base_url=config.OPENAI_API_BASE
            )
            self.model = config.MODEL_NAME
            self.max_tokens = config.MAX_TOKENS
            self.temperature = config.TEMPERATURE
            logger.info("FeedbackAgent 初始化成功")
        except Exception as e:
            logger.error(f"FeedbackAgent 初始化失败: {type(e).__name__}: {e}")
            raise

    def validate_input(self, course_content: str, student_performance: str) -> bool:
        logger.info("开始验证输入参数")
        # logger.debug(f"课程内容长度: {len(course_content) if course_content else 0}")
        # logger.debug(f"学员表现长度: {len(student_performance) if student_performance else 0}")

        if not course_content or not course_content.strip():
            logger.error("验证失败: 课程内容为空")
            raise ValueError("课程内容不能为空")
        if not student_performance or not student_performance.strip():
            logger.error("验证失败: 学员表现为空")
            raise ValueError("学员表现不能为空")
        if len(course_content) < 10:
            logger.error(f"验证失败: 课程内容过短 ({len(course_content)} 字符)")
            raise ValueError("课程内容过于简短，请提供更详细的信息")
        if len(student_performance) < 10:
            logger.error(f"验证失败: 学员表现过短 ({len(student_performance)} 字符)")
            raise ValueError("学员表现描述过于简短，请提供更详细的信息")

        logger.info("输入验证通过")
        return True

    def generate_report(self, course_content: str, student_performance: str) -> str:
        logger.info("=" * 60)
        logger.info("开始生成报告 (非流式)")
        self.validate_input(course_content, student_performance)

        user_prompt = USER_PROMPT_TEMPLATE.format(
            course_content=course_content,
            student_performance=student_performance
        )

        logger.debug(f"System Prompt 长度: {len(SYSTEM_PROMPT)}")
        logger.debug(f"User Prompt 长度: {len(user_prompt)}")
        logger.info(f"调用 API: {self.model}")
        logger.debug(f"API 参数: max_tokens={self.max_tokens}, temperature={self.temperature}")

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_prompt}
                ],
                max_tokens=self.max_tokens,
                temperature=self.temperature,
                stream=False
            )
            logger.info("API 调用成功")
            logger.debug(f"响应 ID: {response.id}")
            logger.debug(f"模型: {response.model}")
            logger.debug(f"Token 使用: prompt={response.usage.prompt_tokens}, completion={response.usage.completion_tokens}, total={response.usage.total_tokens}")

            content = response.choices[0].message.content.strip()
            logger.info(f"报告生成成功，长度: {len(content)} 字符")
            return content
        except Exception as e:
            logger.error(f"API 调用失败: {type(e).__name__}: {e}")
            if hasattr(e, 'response'):
                logger.error(f"响应状态码: {e.response.status_code if hasattr(e.response, 'status_code') else '未知'}")
                logger.error(f"响应内容: {e.response.text if hasattr(e.response, 'text') else '未知'}")
            raise

    def generate_report_streaming(self, course_content: str, student_performance: str):
        logger.info("=" * 60)
        logger.info("开始生成报告 (流式)")
        self.validate_input(course_content, student_performance)

        user_prompt = USER_PROMPT_TEMPLATE.format(
            course_content=course_content,
            student_performance=student_performance
        )

        logger.debug(f"System Prompt 长度: {len(SYSTEM_PROMPT)}")
        logger.debug(f"User Prompt 长度: {len(user_prompt)}")
        logger.info(f"调用 API (流式): {self.model}")
        logger.debug(f"API 参数: max_tokens={self.max_tokens}, temperature={self.temperature}")

        try:
            stream = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_prompt}
                ],
                max_tokens=self.max_tokens,
                temperature=self.temperature,
                stream=True
            )
            logger.info("API 连接成功，开始接收流式数据...")

            chunk_count = 0
            total_content = ""

            for chunk in stream:
                if chunk.choices[0].delta.content:
                    content = chunk.choices[0].delta.content
                    total_content += content
                    chunk_count += 1
                    if chunk_count % 10 == 0:
                        logger.debug(f"已接收 {chunk_count} 个数据块，当前长度: {len(total_content)} 字符")
                    yield content

            logger.info(f"流式报告生成成功，共 {chunk_count} 个数据块，总长度: {len(total_content)} 字符")

        except Exception as e:
            logger.error(f"流式 API 调用失败: {type(e).__name__}: {e}")
            if hasattr(e, 'response'):
                logger.error(f"响应状态码: {e.response.status_code if hasattr(e.response, 'status_code') else '未知'}")
                logger.error(f"响应内容: {e.response.text if hasattr(e.response, 'text') else '未知'}")
            raise