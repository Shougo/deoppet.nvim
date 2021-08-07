import {
  BaseSource,
  Candidate,
  Context,
  Denops,
  SourceOptions,
} from "https://deno.land/x/ddc_vim@v0.0.11/types.ts";

export class Source extends BaseSource {
  async gatherCandidates(
    denops: Denops,
    _context: Context,
    _options: SourceOptions,
    _params: Record<string, unknown>,
  ): Promise<Candidate[]> {
    return [];
  }
}
