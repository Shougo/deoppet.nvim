import {
  BaseSource,
  Context,
  Item,
} from "https://deno.land/x/ddc_vim@v3.9.0/types.ts";
import { Denops, fn, vars } from "https://deno.land/x/ddc_vim@v3.9.0/deps.ts#^";

type Params = Record<never, never>;

export class Source extends BaseSource<Params> {
  override async gather(args: {
    denops: Denops;
    context: Context;
  }): Promise<Item[]> {
    const snippets = await vars.b.get(
      args.denops,
      "deoppet_snippets",
    ) as Record<
      string,
      unknown
    >[];
    if (!snippets) {
      return [];
    }

    const wordMatch = /\w+$/.exec(args.context.input);
    const charsMatch = /\S+$/.exec(args.context.input);
    const isWord = wordMatch && charsMatch && wordMatch[0] == charsMatch[0];

    const ret: Record<string, Item> = {} as Record<string, Item>;
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

      const options = val.options as Record<string, Item>;
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

  override params(): Params {
    return {};
  }
}
