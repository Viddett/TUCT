namespace BlazorApp1.Data
{
    public class LED
    {

        private int _red;
        private int _green;
        private int _blue;
        private int _intens;

        private int banan;

        public int red { get { return this._red; } }
        public int green { get { return this._green; } }
        public int blue { get { return this._blue; } }

        public void set_rgb(int red, int green, int blue) {
            int rgb_max = 255;
            this._red = limit_val(red,rgb_max);
            this._green = limit_val(green, rgb_max);
            this._blue = limit_val(blue, rgb_max);
        }

        public void set_intens(int intens)
        {
            this._intens= limit_val(32, intens);
        }

        public void set_led(int red, int green,int blue, int intens){
            this.set_rgb(red, green, blue);
            this.set_intens(intens);
        }

        private int limit_val(int val,int limit)
        {
            if (val > limit) {
                val = limit;
            }
            return val;
        }

        public int[] get_rgb()
        {
            return new int[3]{ this._red,this._green,this._blue};
        }

        public int get_intens() { 
            return this._intens;
        }


    }
}
