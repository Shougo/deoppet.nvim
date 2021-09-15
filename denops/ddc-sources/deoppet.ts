import {
  BaseSource,
  Candidate,
  Context,
} from "https://deno.land/x/ddc_vim@v0.5.0/types.ts";
import {
  Denops,
  fn,
  vars,
} from "https://deno.land/x/ddc_vim@v0.5.0/deps.ts#^";

export class Source extends BaseSource {
  async gatherCandidates(args: {
    denops: Denops,
    context: Context,
  }): Promise<Candidate[]> {
    const snippets = await vars.b.get(args.denops, "deoppet_snippets") as Record<
      string,
      unknown
    >[];
    if (!snippets) {
      return [];
    }

    const wordMatch = /\w+$/.exec(args.context.input);
    const charsMatch = /\S+$/.exec(args.context.input);
    const isWord = wordMatch && charsMatch && wordMatch[0] == charsMatch[0];

    const ret: Record<string, Candidate> = {} as Record<string, Candidate>;
    for (const key in snippets) {
      const val = snippets[key];
      const menu = val.abbr
        ? (val.abbr as string)
        : (val.text as string).replaceAll(/\n/g, "");

      const triggerCandidates = [val.trigger].concat(val.alias ? val.alias : [])
        .map((v) => ({
          word: v as string,
          menu: menu,
        }));

      const options = val.options as Record<string, Candidate>;
      if (
        (!options.head || /^\s*\S+$/.test(args.context.input)) &&
        (!options.word || isWord) &&
        (!val.regexp ||
          await fn.matchstr(args.denops, args.context.input, val.regexp) != "")
      ) {
        for (const candidate of triggerCandidates) {
          const word = candidate.word as string;
          if (!(word in ret)) {
            ret[word] = candidate;
          }
        }
      }
    }
    return Object.values(ret);
  }
}
