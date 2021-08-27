import {
  BaseSource,
  Candidate,
  Context,
  DdcOptions,
  SourceOptions,
} from "https://deno.land/x/ddc_vim@v0.0.13/types.ts";
import {
  Denops,
  fn,
  vars,
} from "https://deno.land/x/ddc_vim@v0.0.13/deps.ts#^";

export class Source extends BaseSource {
  async gatherCandidates(
    denops: Denops,
    context: Context,
    _ddcOptions: DdcOptions,
    _sourceOptions: SourceOptions,
    _sourceParams: Record<string, unknown>,
    _completeStr: string,
  ): Promise<Candidate[]> {
    const snippets = await vars.b.get(denops, "deoppet_snippets") as Record<
      string,
      unknown
    >[];
    if (!snippets) {
      return [];
    }

    const wordMatch = /\w+$/.exec(context.input);
    const charsMatch = /\S+$/.exec(context.input);
    const isWord = wordMatch && charsMatch && wordMatch[0] != charsMatch[0];

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
          dup: true,
        }));

      const options = val.options as Record<string, Candidate>;
      if (
        (!options.head || /^\s*\S+$/.test(context.input)) &&
        (!options.word || isWord) &&
        (!val.regexp ||
          await fn.matchstr(denops, context.input, val.regexp) != "")
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
