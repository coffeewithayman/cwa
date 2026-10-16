// ---------------------------------------------------------------------------
// PRESS — written coverage (articles, book chapters, …) for /press.
// Videos and podcasts belong on /talks instead.
//
// To add an entry: drop an image in src/assets/press/, import it below, and
// append an object. The page sorts newest first, so order here doesn't matter.
// ---------------------------------------------------------------------------
import type { ImageMetadata } from "astro";
import scMediaSiem from "../assets/press/sc-media-siem-fatigue.jpg";
import tribeOfHackers from "../assets/press/tribe-of-hackers-blue-team.jpg";

export interface PressItem {
  id: string;
  title: string;
  outlet: string;
  /** Short label shown as a chip, e.g. "Article", "Book chapter". */
  kind: string;
  /** What Ayman's part was, e.g. "Quoted", "Contributing author". */
  role: string;
  /** ISO date (YYYY-MM-DD or YYYY-MM). */
  date: string;
  href: string;
  /** Call-to-action text, e.g. "Read on SC Media". */
  linkLabel: string;
  image: ImageMetadata;
  imageAlt: string;
  /**
   * "wide" for landscape hero art (cropped to fill the frame);
   * "cover" for portrait book covers (shown whole on a blurred backdrop).
   */
  imageFit: "wide" | "cover";
  /** One or two sentences of context. */
  blurb: string;
  /** Optional pull quote, verbatim from the piece. */
  quote?: string;
}

export const press: PressItem[] = [
  {
    id: "tribe-of-hackers-blue-team",
    title: "Tribe of Hackers Blue Team: Tribal Knowledge from the Best in Defensive Cybersecurity",
    outlet: "Wiley",
    kind: "Book chapter",
    role: "Contributing author · Chapter 13",
    date: "2020-09",
    href: "https://www.oreilly.com/library/view/tribe-of-hackers/9781119643418/c13.xhtml",
    linkLabel: "Read the chapter on O’Reilly",
    image: tribeOfHackers,
    imageAlt: "Cover of Tribe of Hackers Blue Team by Marcus J. Carey and Jennifer Jin",
    imageFit: "cover",
    blurb:
      "Marcus J. Carey and Jennifer Jin’s collection of interviews with defenders from across the industry, each answering the same set of questions about blue team work and careers.",
  },
  {
    id: "sc-media-siem-fatigue",
    title: "Reducing SIEM fatigue: Finding a signal in all the noise",
    outlet: "SC Media",
    kind: "Article",
    role: "Quoted as a subject-matter expert",
    date: "2019-08-07",
    href: "https://www.scworld.com/news/reducing-siem-fatigue",
    linkLabel: "Read on SC Media",
    image: scMediaSiem,
    imageAlt: "Illustration of an eye peering through a keyhole over a waveform on a laptop screen",
    imageFit: "wide",
    blurb:
      "Lee Sustar on how SOCs cope with the flood of SIEM alerts, including how cloud logs change the picture and what it takes to tune a SIEM for them.",
    quote:
      "It’s a tool. At the end of the day, you need good SOC analysts who have the ability to find this nuanced behavior.",
  },
];
