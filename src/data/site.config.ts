// ---------------------------------------------------------------------------
// SITE CONFIG — edit everything about the network graph from this one file.
// ---------------------------------------------------------------------------

export interface NodeConfig {
  /** Unique id, used as the React/Astro key — keep it short and stable. */
  id: string;
  /** Main label. Use "\n" to force a line break (e.g. "Cloud Security\nLabs"). */
  mainText: string;
  /** Small caption under the main text, e.g. "ADVISORY". */
  secondaryText: string;
  /** Shown on hover. */
  tooltip: string;
  /** Where the node links to. Opens in a new tab. Ignored (use "#") when `children` is set — the node expands instead of navigating. */
  href: string;
  /** Diameter in px. Falls back to theme.defaultNodeSize if omitted. */
  size?: number;
  /** Ring/text accent color for this node. Falls back to theme.defaultRingColor if omitted. */
  ringColor?: string;
  /**
   * Optional sub-bubbles. When set (non-empty), this node renders as an
   * expandable button on desktop (fans out into these sub-bubbles on click)
   * and as a <details>/<summary> accordion on mobile, instead of linking out
   * directly.
   */
  children?: SubNodeConfig[];
}

export interface SubNodeConfig {
  /** Unique id across ALL nodes and sub-nodes site-wide. */
  id: string;
  mainText: string;
  secondaryText: string;
  tooltip: string;
  href: string;
  /** Falls back to the PARENT node's ring color (not theme.defaultRingColor) if omitted. */
  ringColor?: string;
}

export interface CenterNodeConfig {
  name: string;
  title: string;
  /** Optional extra line(s) of text under the title. Use "\n" for line breaks. */
  extraText?: string;
  /** Optional call-to-action button. This is the only allowed link on the center node. */
  cta?: {
    label: string;
    href: string;
  };
}

export interface ThemeConfig {
  /** Page background color. */
  backgroundColor: string;
  /** Radial glow color behind the center node ("inside space color"). */
  innerGlowColor: string;
  /** Default outer ring color for satellite nodes (overridable per-node). */
  defaultRingColor: string;
  /** Default node diameter in px (overridable per-node). */
  defaultNodeSize: number;
  /** Primary text color (main text, headings). */
  textColor: string;
  /** Secondary/muted text color (captions, labels). */
  secondaryTextColor: string;
  /** Color of the dotted connecting lines. */
  lineColor: string;
  /** Center node ring color. */
  centerRingColor: string;
  /** Center node diameter in px. */
  centerNodeSize: number;
  /** CTA button background color. */
  ctaBackgroundColor: string;
  /** CTA button text color. */
  ctaTextColor: string;
}

export const theme: ThemeConfig = {
  backgroundColor: "#0a0a0a",
  innerGlowColor: "#1a5c3f",
  defaultRingColor: "#3a8f6f",
  defaultNodeSize: 160,
  textColor: "#f2f2f2",
  secondaryTextColor: "#8a8a8a",
  lineColor: "#3a3a3a",
  centerRingColor: "#3ddc84",
  centerNodeSize: 190,
  ctaBackgroundColor: "#3ddc84",
  ctaTextColor: "#0a0a0a",
};

export const centerNode: CenterNodeConfig = {
  name: "Ayman\nElsawah",
  title: "Head of Security & CISO | Educator",
  extraText: "Helping people build and understand security.",
  // cta: {
  //   label: "Book a call",
  //   href: "https://cal.com/aymanelsawah",
  // },
};

// Add or remove entries here to add/remove nodes — the circular layout
// recalculates automatically based on how many nodes are in this array.
export const nodes: NodeConfig[] = [
  // {
  //   id: "cloud-security-labs",
  //   mainText: "Cloud Security\nLabs",
  //   secondaryText: "ADVISORY",
  //   tooltip: "Fractional CISO & cloud security advisory work",
  //   href: "https://cloudsecuritylabs.io",
  //   ringColor: "#3ddc84",
  // },
  {
    id: "security-cafe",
    mainText: "The Security\nCafe",
    secondaryText: "NEWSLETTER",
    tooltip: "Substack newsletter on security leadership,  careers, and industry insights",
    href: "https://securitycafe.io",
    ringColor: "#4a9eff",
  },
  {
    id: "breaking-in",
    mainText: "Breaking IN: A Practical Guide to Breaking Into Infosec",
    secondaryText: "BOOK",
    tooltip: "My personal guide to breaking into the information security field",
    href: "https://breakingintoinfosec.com/",
    ringColor: "#d4a72c",
  },
  {
    id: "getting-into-infosec",
    mainText: "Getting Into Infosec",
    secondaryText: "PODCAST",
    tooltip: "Podcast interviewing security professionals as there is no one path into infosec",
    href: "https://gettingintoinfosec.com",
    ringColor: "#e8622c",
  },
  // {
  //   id: "zero-trust-101",
  //   mainText: "Zero Trust 101",
  //   secondaryText: "COURSE",
  //   tooltip: "Online course covering zero trust fundamentals",
  //   href: "https://zerotrust101.com",
  //   ringColor: "#9b59d0",
  // },
  {
    id: "Enterprise-Security-Weekly",
    mainText: "Eneterprise Security Weekly Co-Host",
    secondaryText: "SPEAKING",
    tooltip: "Co-Host with Host Adrian Sanabria on the Enterprise Security Weekly Podcast",
    href: "https://youtu.be/o-Edp9puMEo?si=71SjUt1akYGDx4vH&t=2340",
    ringColor: "#3ddc84",
  },
  {
    id: "fractional-ciso-course",
    mainText: "Fractional CISO\nCourse",
    secondaryText: "COURSE",
    tooltip: "Course on becoming a fractional/virtual CISO",
    href: "https://securitycafe.thinkific.com/courses/vciso-fractional-ciso-course",
    ringColor: "#9b59d0",
  },
  {
    id: "misc-projects",
    mainText: "Misc\nProjects",
    secondaryText: "GITHUB",
    tooltip: "A few smaller side projects and experiments — click to expand",
    href: "#", // unused — this node expands via `children` instead of navigating
    ringColor: "#8a8a8a",
    children: [
      {
        id: "sleuthr",
        mainText: "Sleuthr",
        secondaryText: "GITHUB",
        tooltip: "Domain-wide audit tool that finds Google Drive files publicly shared across your Google Workspace, with automated lockdown options",
        href: "https://github.com/coffeewithayman/sleuthr",
      },
      {
        id: "pong",
        mainText: "Pong",
        secondaryText: "GITHUB",
        tooltip: "Real-time multiplayer Pong with a queue system, persistent leaderboard, and spectator mode — playable in the browser",
        href: "https://github.com/coffeewithayman/pong",
      },
      {
        id: "visualizer",
        mainText: "Visualizer",
        secondaryText: "GITHUB",
        tooltip: "Real-time audio visualizer that turns microphone input into colorful, customizable frequency bars",
        href: "https://github.com/coffeewithayman/visualizer",
      },
    ],
  },
  // {
  //   id: "security-cafe-circle",
  //   mainText: "Security Cafe Circle",
  //   secondaryText: "COMMUNITY",
  //   tooltip: "Community for security professionals",
  //   href: "https://securitycafe.io/chat ",
  //   ringColor: "#4a9eff",
  // },
];

export const chrome = {
  headerLabel: "Ayman Elsawah (@coffeewithayman)",
  aboutTitle: "About Ayman",
  // Markdown supported: **bold**, _italic_, [links](https://...), multiple paragraphs.
  aboutTextMarkdown: `Everything I make connects back to one idea: helping people and companies build and understand security. 
  
  Many years in, still adding nodes.`,
  elsewhereTitle: "ELSEWHERE",
  // One entry per link. `icon` picks the matching glyph rendered in
  // ElsewhereList.astro (see the `icons` map there for the supported keys).
  elsewhereLinks: [
    { label: "Twitter / X", href: "https://twitter.com/coffeewithayman", icon: "x" },
    { label: "LinkedIn", href: "https://linkedin.com/in/infosecleader", icon: "linkedin" },
    { label: "YouTube", href: "https://youtube.com/@coffeewithayman", icon: "youtube" },
    { label: "Instagram", href: "https://instagram.com/coffeewithayman", icon: "instagram" },
    { label: "GitHub", href: "https://github.com/coffeewithayman", icon: "github" },
    { label: "RSS feed", href: "https://securitycafe.io/feed", icon: "rss" },
  ] satisfies { label: string; href: string; icon: string }[],
  footerText: `© ${new Date().getFullYear()} Ayman Elsawah`,
  // footerRight: "rendered as force graph · static preview",
};
