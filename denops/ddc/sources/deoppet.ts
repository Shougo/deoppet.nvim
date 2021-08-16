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
    let snippets = await vars.b.get(denops, "deoppet_snippets") as Record<string, unknown>[];
    if (!snippets) {
      return [];
    }

    const wordMatch = /\w+$/.exec(context.input);
    const charsMatch = /\S+$/.exec(context.input);
    const isWord = wordMatch && charsMatch && wordMatch[0] != charsMatch[0];

    let ret: Candidate[] = [];
    for (const key in snippets) {
      const val = snippets[key];
      const menu = val.abbr ? val.abbr : val.text.replaceAll(/\n/g, '');

      const triggerCandidates = [val.trigger].concat(val.alias ? val.alias : [])
        .map((v) => ({
          word: v,
          menu: menu,
          dup: true,
        }));

      if (
        (!val.options.head || /^\s*\S+$/.test(context.input)) &&
        (!val.options.word || isWord) &&
        (!val.regexp || await fn.matchstr(denops, context.input, val.regexp) != "")
      ) {
        ret = ret.concat(triggerCandidates);
      }
    }
    return ret;
  }
}
