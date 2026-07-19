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
  /** Where the node links to. Opens in a new tab. */
  href: string;
  /** Diameter in px. Falls back to theme.defaultNodeSize if omitted. */
  size?: number;
  /** Ring/text accent color for this node. Falls back to theme.defaultRingColor if omitted. */
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
  defaultNodeSize: 120,
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
  title: "Fractional CISO",
  cta: {
    label: "Book a call",
    href: "https://cal.com/aymanelsawah",
  },
};

// Add or remove entries here to add/remove nodes — the circular layout
// recalculates automatically based on how many nodes are in this array.
export const nodes: NodeConfig[] = [
  {
    id: "cloud-security-labs",
    mainText: "Cloud Security\nLabs",
    secondaryText: "ADVISORY",
    tooltip: "Fractional CISO & cloud security advisory work",
    href: "https://cloudsecuritylabs.io",
    ringColor: "#3ddc84",
  },
  {
    id: "security-cafe",
    mainText: "The Security\nCafe",
    secondaryText: "NEWSLETTER",
    tooltip: "Weekly newsletter on security careers and practice",
    href: "https://securitycafe.io",
    ringColor: "#4a9eff",
  },
  {
    id: "breaking-in",
    mainText: "Breaking IN",
    secondaryText: "BOOK",
    tooltip: "Book on breaking into the security industry",
    href: "https://breakinginbook.com",
    ringColor: "#d4a72c",
  },
  {
    id: "getting-into-infosec",
    mainText: "Getting Into Infosec",
    secondaryText: "PODCAST",
    tooltip: "Podcast interviewing security professionals",
    href: "https://gettingintoinfosec.com",
    ringColor: "#e8622c",
  },
  {
    id: "zero-trust-101",
    mainText: "Zero Trust 101",
    secondaryText: "COURSE",
    tooltip: "Online course covering zero trust fundamentals",
    href: "https://zerotrust101.com",
    ringColor: "#9b59d0",
  },
  {
    id: "talks-press",
    mainText: "Talks & Press",
    secondaryText: "SPEAKING",
    tooltip: "Conference talks, interviews, and press coverage",
    href: "https://cloudsecuritylabs.io/talks",
    ringColor: "#3ddc84",
  },
  {
    id: "security-cafe-circle",
    mainText: "Security Cafe Circle",
    secondaryText: "COMMUNITY",
    tooltip: "Community for security professionals",
    href: "https://securitycafe.io/circle",
    ringColor: "#4a9eff",
  },
];

export const chrome = {
  headerLabel: "AYMAN.NETWORK",
  aboutTitle: "ABOUT THIS NETWORK",
  // Markdown supported: **bold**, _italic_, [links](https://...), multiple paragraphs.
  aboutTextMarkdown: `Everything I make connects back to one idea: helping people build and understand security. 17 years in, still adding nodes — advisory work, writing, a podcast, a course, a community.`,
  elsewhereTitle: "ELSEWHERE",
  // Markdown supported: write a bullet list of links, one per line.
  elsewhereLinksMarkdown: `
- [Twitter / X](https://twitter.com/)
- [LinkedIn](https://linkedin.com/)
- [YouTube](https://youtube.com/)
- [Instagram](https://instagram.com/)
- [RSS feed](/rss.xml)
`,
  footerText: `© ${new Date().getFullYear()} Ayman Elsawah`,
  footerRight: "rendered as force graph · static preview",
};
