import {
  Layout,
  Menu,
  Button,
  Badge,
  Modal,
  Spin,
  Tooltip,
  type MenuProps,
} from "antd";
import { useState, useEffect, useCallback } from "react";
import { useNavigate } from "react-router-dom";
import { useTranslation } from "react-i18next";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import {
  MessageSquare,
  Radio,
  Zap,
  MessageCircle,
  Wifi,
  UsersRound,
  CalendarClock,
  Activity,
  Sparkles,
  Briefcase,
  Cpu,
  Box,
  Globe,
  Settings,
  Plug,
  PanelLeftClose,
  PanelLeftOpen,
  Copy,
  Check,
} from "lucide-react";
import api from "../api";
import styles from "./index.module.less";

const { Sider } = Layout;

const PYPI_URL = "https://pypi.org/pypi/test_with_ai/json";

const DEFAULT_OPEN_KEYS = [
  "chat-group",
  "control-group",
  "agent-group",
  "settings-group",
];

const KEY_TO_PATH: Record<string, string> = {
  chat: "/chat",
  channels: "/channels",
  sessions: "/sessions",
  "cron-jobs": "/cron-jobs",
  heartbeat: "/heartbeat",
  skills: "/skills",
  mcp: "/mcp",
  workspace: "/workspace",
  models: "/models",
  environments: "/environments",
  "agent-config": "/agent-config",
};

const UPDATE_MD: Record<string, string> = {
  zh: `### Test with AI如何更新

要更�?Test with AI 到最新版本，可根据你的安装方式选择对应方法�?

1. 如果你使用的是一键安装脚本，直接重新运行安装命令即可自动升级�?

2. 如果你是通过 pip 安装，在终端中执行以下命令升级：

\`\`\`
pip install --upgrade test_with_ai
\`\`\`

3. 如果你是从源码安装，进入项目目录并拉取最新代码后重新安装�?

\`\`\`
cd Test with AI
git pull origin main
pip install -e .
\`\`\`

4. 如果你使用的�?Docker，拉取最新镜像并重启容器�?

\`\`\`
docker pull agentscope/test_with_ai:latest
docker run -p 127.0.0.1:8088:8088 -v test_with_ai-data:/app/working agentscope/test_with_ai:latest
\`\`\`

升级后重启服�?test_with_ai app。`,

  ru: `### Как обновить Test with AI

Чтобы обновить Test with AI, выберите способ в зависимости от типа установки:

1. Если вы устанавливали через однострочный скрипт, повторно запустите установщик для обновления.

2. Если устанавливали через pip, выполните:

\`\`\`
pip install --upgrade test_with_ai
\`\`\`

3. Если устанавливали из исходников, получите последние изменения и переустановите:

\`\`\`
cd Test with AI
git pull origin main
pip install -e .
\`\`\`

4. Если используете Docker, загрузите новый образ и перезапустите контейнер:

\`\`\`
docker pull agentscope/test_with_ai:latest
docker run -p 127.0.0.1:8088:8088 -v test_with_ai-data:/app/working agentscope/test_with_ai:latest
\`\`\`

После обновления перезапустите сервис с помощью \`test_with_ai app\`.`,

  en: `### How to update Test with AI

To update Test with AI, use the method matching your installation type:

1. If installed via one-line script, re-run the installer to upgrade.

2. If installed via pip, run:

\`\`\`
pip install --upgrade test_with_ai
\`\`\`

3. If installed from source, pull the latest code and reinstall:

\`\`\`
cd Test with AI
git pull origin main
pip install -e .
\`\`\`

4. If using Docker, pull the latest image and restart the container:

\`\`\`
docker pull agentscope/test_with_ai:latest
docker run -p 127.0.0.1:8088:8088 -v test_with_ai-data:/app/working agentscope/test_with_ai:latest
\`\`\`

After upgrading, restart the service with \`test_with_ai app\`.`,
};

interface SidebarProps {
  selectedKey: string;
}

function CopyButton({ text }: { text: string }) {
  const [copied, setCopied] = useState(false);
  const { t } = useTranslation();

  const handleCopy = useCallback(() => {
    navigator.clipboard.writeText(text).then(() => {
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    });
  }, [text]);

  return (
    <Tooltip
      title={copied ? t("common.copied", "Copied!") : t("common.copy", "Copy")}
    >
      <Button
        type="text"
        size="small"
        icon={copied ? <Check size={13} /> : <Copy size={13} />}
        onClick={handleCopy}
        className={`${styles.copyBtn} ${
          copied ? styles.copyBtnCopied : styles.copyBtnDefault
        }`}
      />
    </Tooltip>
  );
}

export default function Sidebar({ selectedKey }: SidebarProps) {
  const navigate = useNavigate();
  const { t, i18n } = useTranslation();
  const [collapsed, setCollapsed] = useState(false);
  const [openKeys, setOpenKeys] = useState<string[]>(DEFAULT_OPEN_KEYS);
  const [version, setVersion] = useState<string>("");
  const [latestVersion, setLatestVersion] = useState<string>("");
  const [allVersions, setAllVersions] = useState<string[]>([]);
  const [updateModalOpen, setUpdateModalOpen] = useState(false);
  const [updateMarkdown, setUpdateMarkdown] = useState<string>("");

  useEffect(() => {
    if (!collapsed) {
      setOpenKeys(DEFAULT_OPEN_KEYS);
    }
  }, [collapsed]);

  useEffect(() => {
    api
      .getVersion()
      .then((res) => setVersion(res?.version ?? ""))
      .catch(() => {});
  }, []);

  useEffect(() => {
    fetch(PYPI_URL)
      .then((res) => res.json())
      .then((data) => {
        const releases = data?.releases ?? {};
        // Sort versions by upload_time (newest first)
        const versionsWithTime = Object.entries(releases).map(
          ([version, files]) => {
            const fileList = files as Array<{ upload_time_iso_8601?: string }>;
            // Get the latest upload time among all files for this version
            const latestUpload = fileList
              .map((f) => f.upload_time_iso_8601)
              .filter(Boolean)
              .sort()
              .pop();
            return { version, uploadTime: latestUpload || "" };
          },
        );
        versionsWithTime.sort(
          (a, b) =>
            new Date(b.uploadTime).getTime() - new Date(a.uploadTime).getTime(),
        );
        const versions = versionsWithTime.map((v) => v.version);
        const latest = versions[0] ?? data?.info?.version ?? "";
        setAllVersions(versions);
        setLatestVersion(latest);
      })
      .catch(() => {});
  }, []);

  const hasUpdate =
    version &&
    allVersions.length > 0 &&
    allVersions.includes(version) &&
    version !== latestVersion;

  const handleOpenUpdateModal = () => {
    setUpdateMarkdown("");
    setUpdateModalOpen(true);
    const lang = i18n.language?.startsWith("zh")
      ? "zh"
      : i18n.language?.startsWith("ru")
      ? "ru"
      : "en";
    const faqLang = lang === "zh" ? "zh" : "en";
    const url = `https://test_with_ai.agentscope.io/docs/faq.${faqLang}.md`;
    fetch(url, { cache: "no-cache" })
      .then((res) => (res.ok ? res.text() : Promise.reject()))
      .then((text) => {
        const zhPattern = /###\s*Test with AI如何更新[\s\S]*?(?=\n###|$)/;
        const enPattern = /###\s*How to update Test with AI[\s\S]*?(?=\n###|$)/;
        const match = text.match(faqLang === "zh" ? zhPattern : enPattern);
        setUpdateMarkdown(
          match && lang !== "ru"
            ? match[0].trim()
            : UPDATE_MD[lang] ?? UPDATE_MD.en,
        );
      })
      .catch(() => {
        setUpdateMarkdown(UPDATE_MD[lang] ?? UPDATE_MD.en);
      });
  };

  const menuItems: MenuProps["items"] = [
    {
      key: "chat-group",
      label: t("nav.chat"),
      icon: <MessageSquare size={16} />,
      children: [
        {
          key: "chat",
          label: t("nav.chat"),
          icon: <MessageCircle size={16} />,
        },
      ],
    },
    {
      key: "control-group",
      label: t("nav.control"),
      icon: <Radio size={16} />,
      children: [
        { key: "channels", label: t("nav.channels"), icon: <Wifi size={16} /> },
        {
          key: "sessions",
          label: t("nav.sessions"),
          icon: <UsersRound size={16} />,
        },
        {
          key: "cron-jobs",
          label: t("nav.cronJobs"),
          icon: <CalendarClock size={16} />,
        },
        {
          key: "heartbeat",
          label: t("nav.heartbeat"),
          icon: <Activity size={16} />,
        },
      ],
    },
    {
      key: "agent-group",
      label: t("nav.agent"),
      icon: <Zap size={16} />,
      children: [
        {
          key: "workspace",
          label: t("nav.workspace"),
          icon: <Briefcase size={16} />,
        },
        { key: "skills", label: t("nav.skills"), icon: <Sparkles size={16} /> },
        { key: "mcp", label: t("nav.mcp"), icon: <Plug size={16} /> },
        {
          key: "agent-config",
          label: t("nav.agentConfig"),
          icon: <Settings size={16} />,
        },
      ],
    },
    {
      key: "settings-group",
      label: t("nav.settings"),
      icon: <Cpu size={16} />,
      children: [
        { key: "models", label: t("nav.models"), icon: <Box size={16} /> },
        {
          key: "environments",
          label: t("nav.environments"),
          icon: <Globe size={16} />,
        },
      ],
    },
  ];

  return (
    <Sider
      collapsed={collapsed}
      onCollapse={setCollapsed}
      width={275}
      className={styles.sider}
    >
      <div className={styles.siderTop}>
        {!collapsed && (
          <div className={styles.logoWrapper}>
            <img src="/logo.png" alt="Test with AI" className={styles.logoImg} />
            {version && (
              <Badge dot={!!hasUpdate} color="red" offset={[4, 18]}>
                <span
                  className={`${styles.versionBadge} ${
                    hasUpdate
                      ? styles.versionBadgeClickable
                      : styles.versionBadgeDefault
                  }`}
                  onClick={() => hasUpdate && handleOpenUpdateModal()}
                >
                  v{version}
                </span>
              </Badge>
            )}
          </div>
        )}
        <Button
          type="text"
          icon={
            collapsed ? (
              <PanelLeftOpen size={20} />
            ) : (
              <PanelLeftClose size={20} />
            )
          }
          onClick={() => setCollapsed(!collapsed)}
          className={styles.collapseBtn}
        />
      </div>

      <Menu
        mode="inline"
        selectedKeys={[selectedKey]}
        openKeys={openKeys}
        onOpenChange={(keys) => setOpenKeys(keys as string[])}
        onClick={({ key }) => {
          const path = KEY_TO_PATH[String(key)];
          if (path) navigate(path);
        }}
        items={menuItems}
      />

      <Modal
        open={updateModalOpen}
        onCancel={() => setUpdateModalOpen(false)}
        title={
          <h3 className={styles.updateModalTitle}>
            {t("sidebar.updateModal.title", { version: latestVersion })}
          </h3>
        }
        width={680}
        footer={[
          <Button
            key="releases"
            type="primary"
            onClick={() =>
              window.open(
                "https://github.com/agentscope-ai/Test with AI/releases",
                "_blank",
              )
            }
            className={styles.updateModalPrimaryBtn}
          >
            {t("sidebar.updateModal.viewReleases")}
          </Button>,
          <Button key="close" onClick={() => setUpdateModalOpen(false)}>
            {t("sidebar.updateModal.close")}
          </Button>,
        ]}
      >
        <div className={styles.updateModalBody}>
          {!updateMarkdown ? (
            <div className={styles.updateModalSpinWrapper}>
              <Spin />
            </div>
          ) : (
            <ReactMarkdown
              remarkPlugins={[remarkGfm]}
              components={{
                code({ className, children, ...props }) {
                  const isBlock =
                    className?.startsWith("language-") ||
                    String(children).includes("\n");
                  if (isBlock) {
                    return (
                      <pre className={styles.codeBlock}>
                        <CopyButton text={String(children)} />
                        <code className={styles.codeBlockInner} {...props}>
                          {children}
                        </code>
                      </pre>
                    );
                  }
                  return (
                    <code className={styles.codeInline} {...props}>
                      {children}
                    </code>
                  );
                },
              }}
            >
              {updateMarkdown}
            </ReactMarkdown>
          )}
        </div>
      </Modal>
    </Sider>
  );
}
