import click, sys, numpy, scipy.misc, os.path, json
from PIL import Image

@click.command()
@click.option('-b', '--black-separator-thickness', default=5)
@click.option('-s', '--min-white-separator-thickness', default=10, type=click.IntRange(5, None))
@click.option('-p', '--max-black-portion', default=5.0)
@click.option('-o', '--output', required=True)
@click.option('-O', '--output-mode', default="single", type=click.Choice(["single","split","json"]))
@click.argument('IMAGE', type=click.Path(exists=True))
def cli(black_separator_thickness, min_white_separator_thickness, max_black_portion, output, output_mode, image):
    """
    Detects likely column boundaries in B/W images.
    """
    # load image
    img = Image.open(open(image,"rb"))
    array = numpy.asarray(img)
    if len(array.shape) != 2:
        click.echo(u"Not a bitonal image. Aborting.", err=True)
        return 1

    click.echo(u"Image dimensions x: %i; y: %i" % (array.shape[0], array.shape[1]), err=True)

    # Localize white separators
    white_separators = []
    white_range_start = 0
    for c in range(0,array.shape[1]):
        black_pixels = 0
        for r in range(0,array.shape[0]):
            if array[r][c] == 0:
                black_pixels += 1
        if black_pixels * 100.0 / array.shape[0] < max_black_portion:
            continue
        elif (c - 1) - white_range_start > min_white_separator_thickness:
            click.echo(u"Found white column from index %i to index %i" % (white_range_start,c - 1), err=True)
            white_separators.append((white_range_start,c - 1))
        white_range_start = c 
    if array.shape[1] - white_range_start > min_white_separator_thickness:
        click.echo(u"Found white column from index %i to index %i" % (white_range_start,array.shape[1]), err=True)
        white_separators.append((white_range_start,c - 1))

    if output_mode == "single":
        # White -> black separators
        array.setflags(write=1)
        black_column = numpy.asarray([0] * array.shape[0])
        for white_separator in white_separators[1:-1]:
            black_separator_start = int((white_separator[1] - white_separator[0]) / 2 - black_separator_thickness / 2)
            for i in range(white_separator[0] + black_separator_start, white_separator[0] + black_separator_start + black_separator_thickness):
                array[:,i] = black_column

        # Save image with black separators
        scipy.misc.imsave(output, array)

    elif output_mode == "split":
        for w in range(0,len(white_separators) - 1):
            clip_l = white_separators[w][0]
            clip_t = 0
            clip_b = array.shape[0]
            clip_r = white_separators[w+1][1]
            click.echo("Cutting image at l: %i, t: %i, r: %i, b: %i" % (clip_l,clip_t,clip_r,clip_b), err=True)
            column = img.crop((clip_l,clip_t,clip_r,clip_b))
            column.save("%s_%02d%s" % (os.path.splitext(output)[0],w,os.path.splitext(output)[1]))

    elif output_mode == "json":
        out_json = {}
        out_json[os.path.basename(image)] = []
        for w in range(0,len(white_separators) - 1):
            clip_l = white_separators[w][0]
            clip_t = 0
            clip_b = array.shape[0]
            clip_r = white_separators[w+1][1]
            click.echo("Found column region at l: %i, t: %i, r: %i, b: %i" % (clip_l,clip_t,clip_r,clip_b), err=True)
            out_json[os.path.basename(image)].append({"l":clip_l,"t":clip_t,"r":clip_r,"b":clip_b})
        json.dump(out_json, open(output, "w"))
            

if __name__ == '__main__':
    cli()
